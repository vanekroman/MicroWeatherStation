from machine import I2C
import time
import neopixel
import uselect, sys
import BG77
import _thread
import ahtx0
import ujson

# wait timeout in seconds for sending JSON data function
WAIT_FOR_BG77_RESPONSE_TIMEOUT = 5;

i2c1 = I2C(1, scl = machine.Pin(15), sda = machine.Pin(14), freq = 400000)
tmp_sensor = ahtx0.AHT20(i2c1)
tmp_sensor.initialize()

spoll=uselect.poll()
spoll.register(sys.stdin,uselect.POLLIN)
pon_trig = machine.Pin(9,machine.Pin.OUT)

# machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5), timeout=200, timeout_char=5)
bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rxbuf=256, rx=machine.Pin(1), timeout = 0, timeout_char=1)
bg_uart.write(bytes("AT\r\n","ascii"))
print(bg_uart.read(10))

module = BG77.BG77(bg_uart, verbose=True, radio = False)
time.sleep(3)

# ADC current reading task
def core2_task():
    sel0 = machine.Pin(2, machine.Pin.OUT)
    sel1 = machine.Pin(3, machine.Pin.OUT)

    sel0.value(0)
    sel1.value(1)

    adc = machine.ADC(0)

    uart = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))
    VREF=3.3
    while True:
        read_adc = adc.read_u16()
        '''
        if read_adc > 65000:
            sel0.value(1)
        elif read_adc < 42000:
            sel0.value(0)
        '''
        #print(str(read_adc))
        uart.write(str(time.ticks_ms())+ "," + str(read_adc)+"\r")
        time.sleep(0.001)

# wait fuction for the CONNECTED status
def waitForCEREG():
    data_out = ""
    while True:
        if bg_uart.any():
            time.sleep(.01)
            data_tmp = bg_uart.read(1)
            if data_tmp:
                data_out = data_out + str(data_tmp, 'ascii')
            if "+CEREG: 5" in data_out:
                time.sleep(.01)
                data_tmp = bg_uart.read()
                data_out = data_out + str(data_tmp, 'ascii')
                print(data_out)
                return

# terminal handling fuction 1
def read1():
    return(sys.stdin.read(1) if spoll.poll(0) else None)

# terminal handling fuction 2
def readline():
    c = read1()
    buffer = ""
    while c != None:
        buffer += c
        c = read1()
    return buffer

# rewriting __read, the BG77 class function in BG77.py library 
# raises OSError when a timeout occurs, without detecting the exit_condition
def __read(self, exit_condition="OK\r\n", timeout = 10) -> str:
    time_start = time.time()
    data_out = ""
    while time.time() < (time_start + timeout):
        data_tmp = self.serial.read(1)
        if data_tmp:
            data_out = data_out + str(data_tmp, 'ascii')
        if exit_condition in data_out:
            return data_out
    # raise OSError("BG77 Timeout: Cannot get the response from the device. TIP: increse timeout")
    # or: return None # None return handling need to be implemented further within the BG77.py library
    return ""

# fuction sends json data to MQTT topic
def sendData_JSON(self, data = {}, topic = "telemetry"):
    msg = ujson.dumps(data)
    if module.sendCommand(f"AT+QMTPUB=1,0,0,0,\"v1/devices/me/" + str(topic) + "\"," + str(len(msg)) + "\r\n", ">", WAIT_FOR_BG77_RESPONSE_TIMEOUT) is "":
        print("BG77 Timeout: Cannot get the response from the device.")
    if module.sendCommand(msg, "+QMTPUB: 1,0,0\r\n", WAIT_FOR_BG77_RESPONSE_TIMEOUT) is "":
        print("BG77 Timeout: Cannot get the response from the device.")

module.setRATType(1, 1)
time.sleep(5)
module.setRadio(1)
time.sleep(1)
module.setAPN("lpwa.vodafone.iot")
waitForCEREG()
module.setOperator(BG77.COPS_MANUAL, BG77.Operator.CZ_VODAFONE)
time.sleep(1)

print(" _______________________ \n")
print("| Micro Weather Station |\n")
print("|_____connecting ...____|\n")

# start new thread for adc current measurement
second_thread = _thread.start_new_thread(core2_task, ())

# Using lambda to bind the function with the module instance
module.sendData_JSON = lambda data, topic: sendData_JSON(module, data, topic)
module.sendData_JSONVARIABLE = lambda variable_name, value, topic: sendData_JSON(module, {variable_name: value}, topic)

# binding rewritten function for BG77
module.__read = lambda exit_condition="OK\r\n", timeout = WAIT_FOR_BG77_RESPONSE_TIMEOUT: __read(module, exit_condition, timeout)

# connect to the MQTT server
module.sendCommand("AT+QCSCON=1\r\n")
module.sendCommand("AT+QMTCFG=\"version\",1,4\r\n")
module.sendCommand("AT+QMTOPEN=1,\"147.229.146.40\",1883\r\n", "+QMTOPEN: 1,0", 5)
module.sendCommand("AT+QMTCONN=1,\"27a26100-fd78-11ee-b0f6-299dee8b9dbf\",\"gCVn0rC7cOM7rxvYfo5l\",\"\"\r\n", "+QMTCONN: 1,0,0", 5)

# send device attributes
device_info = {
    "manufacturer": "micro-weather s.r.o",
    "device-id": 22042024,
    "firmware": 1.0,
}
module.sendData_JSON(device_info, "attributes")

# send gps
gps = {
    "latitude": 49.22666897988828, 
    "longitude": 16.57441810391052,    
}
module.sendData_JSON(gps, "attributes")

# requested PSM delay times
TAU_TIME = "10100001" # 60 s
ACTIVE_TIME = "00001000" # 16 s

# setup power saving mode
module.sendCommand("AT+QPSMS=1,,,\"" + TAU_TIME + "\",\"" + ACTIVE_TIME + "\"\r\n")
data = module.sendCommand("AT+QPSMS?\r\n").strip("\r\nOK\r\n").split(",")
tau_time = data[3].strip("\"")
active_time = data[4].strip("\"")
print("TAU TIME = " + str(tau_time) + "\r\n")
print("ACTIVE TIME= " + str(active_time) + "\r\n")

print(" _______________________ \n")
print("| Micro Weather Station |\n")
print("|_______________________|\n")

while True:
    # terminal handling
    data = readline()
    if len(data) != 0:
        if "WKUP" in data.upper():
            pon_trig.value(1)
            time.sleep(.3)
            pon_trig.value(0)
        elif "TIME" in data:
            print(time.ticks_ms())
        elif "STOP" in data:
            os.exit()
        else:
            print(f"{time.ticks_ms()}: -> " + data.strip("\r\n"))
            bg_uart.write(data[:len(data)-2].encode())
            bg_uart.write("\r\n")

    # BG77 response handling
    if bg_uart.any():
        time.sleep(.01)
        data = bg_uart.read()
        #print(data)
        if data != None:
            #data = data.decode()
            #print(data)
            if 0xff in data:
                m = bytearray(data)
                for i in range(len(m)):
                    if m[i] == 0xff:
                        m[i] = 0
                data = bytes(m)
            data = str(data, 'ascii')
            data = data.strip('\r\n')
            data_split = data.split("\n")
            for line in data_split:
                if line == "\r\n":
                    continue
                print(f"{time.ticks_ms()}: <- {line.strip('\r\n')}")

                # waiting for APP RDY, the wake up call for BG77 module
                if "APP RDY" in line:
                    print("     WAKEUP!!    ")

                    # reconnecting to the network
                    if not module.__setCEREG(4):
                        print("BG77 Error setting CEREG")
                    ret = module.sendCommand(f"AT+CEREG?\r\n", "OK\r\n", 5)

                    module.sendCommand("AT+QCSCON=1\r\n")
                    module.sendCommand("AT+QMTCFG=\"version\",1,4\r\n")
                    module.sendCommand("AT+QMTOPEN=1,\"147.229.146.40\",1883\r\n", "+QMTOPEN: 1,0", 2)
                    module.sendCommand("AT+QMTCONN=1,\"27a26100-fd78-11ee-b0f6-299dee8b9dbf\",\"gCVn0rC7cOM7rxvYfo5l\",\"\"\r\n", "+QMTCONN: 1,0,0", 2)

                    # send data if the modulue is connected
                    if "+CEREG: 4" in ret:
                        nwinfo = module.getNWInfo()
                        if nwinfo is not None:
                            data = {
                                "temperature": tmp_sensor.temperature,
                                "humidity": tmp_sensor.relative_humidity,
                                "rssi": nwinfo.RSSI,
                                "rsrp": nwinfo.RSRP,
                                "sinr": nwinfo.SINR,
                                "band": nwinfo.Band,
                                "cellid": nwinfo.CellID,
                                "tac": nwinfo.TAC,
                                "rat": nwinfo.RAT,
                            }
                            time.sleep(1);
                            module.sendData_JSON(data, "telemetry")
                            print(nwinfo)

    time.sleep(0.1);