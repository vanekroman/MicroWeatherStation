import machine
import uselect, sys, time
from lora_E5 import LoRaE5

spoll=uselect.poll()
spoll.register(sys.stdin,uselect.POLLIN)

#Initialize UART and LoRa Library module
uart1 = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5), timeout=200, timeout_char=5)
lora = LoRaE5(uart = uart1,debug=True)

#Test if the module is responsive
lora.test_at()
lora.get_id()

#uart1.timeout = 1

def read1():
    return(sys.stdin.read(1) if spoll.poll(0) else None)

def readline():
    c = read1()
    buffer = ""
    while c != None:
        buffer += c
        c = read1()
    return buffer

#SETUP
print("Setup - Start")
# credditals for station 9
lora.set_id('DevEui', '70B3D57ED004E4E1')
lora.set_id('DevAddr', '260B990D')
lora.set_key('NWKSKEY', 'F5DBC4012F5192468520B3FD576A5C17')
lora.set_key('APPSKEY', '14D02A5FE5167CA087213E1EB58E2DC0')

lora.set_port(1)
lora.set_dr_band('EU868')
lora.set_mode('LWABP')
lora.set_dr(0)
lora.enable_channel(0)
lora.enable_channel(1)
lora.get_enabled_channels()
#lora.set_port(55)
lora.set_counters(0, 0)
lora.set_etsi_duty_cycle(True)


print("Setup - End")
print("Terminal Ready")

#MAIN LOOP
while True:
    data = readline()
    if len(data) != 0:
        print(f"{time.ticks_ms()}: -> " + data)
        uart1.write(data.encode())
    data = uart1.read()
    if data != None:
        data = data.decode()
        data = data.strip('\r\n')
        data_split = data.split("\n")
        for line in data_split:
            if line == "\r\n":
                continue
            print(f"{time.ticks_ms()}: <- {line.strip('\r\n')}")