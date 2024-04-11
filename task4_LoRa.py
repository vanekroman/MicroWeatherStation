from machine import Pin, I2C
import time
from lora_E5 import LoRaE5
import ahtx0


print("Setup - Start")


#Initialize peripherals
led = Pin(15, Pin.OUT)
led.value(0)
i2c1 = I2C(1, scl = Pin(3), sda = Pin(2), freq = 400000)
tmp_sensor = ahtx0.AHT20(i2c1)
tmp_sensor.initialize()


lora = LoRaE5(tx_pin=4, rx_pin=5, speed=9600,debug=True)



lora.test_at()
lora.get_id()

#AVAILABLE COMMANDS WITH EXAMPLES
#lora.set_id('DevAddr', '32303C9E')
# lora.get_version()
# lora.send_ascii("Test", False)
# lora.set_port(128)
# lora.get_port()
# lora.get_adr()
# lora.set_adr(False)
# lora.get_dr()
# lora.set_dr(5)
# lora.get_band_scheme()
# lora.get_all_channels()
# lora.get_channel(2)
# lora.get_enabled_channels()
# lora.get_power()
# lora.set_power(10)
# lora.get_power_map()
# lora.get_ret_limit()
# lora.get_rx2()
# lora.set_rx2(869525000, 5)
# lora.set_id('DevEui', '0004A30B00286CF6')
# lora.set_id('DevAddr', '26011460')

# lora.set_key('NWKSKEY', '2BB9329DB9D0497A4F1301C83D5D3C35')
# lora.set_key('APPSKEY', 'A8AF3A28305A188FD86AE5E638746371')

# lora.set_dr_band('EU868')
# lora.set_mode('LWABP')
# lora.set_dr(0)
# lora.enable_channel(0)
# lora.enable_channel(1)
# lora.enable_channel(2)
# lora.get_enabled_channels()
# lora.set_port(55)
# lora.set_counters(32, 32)
# lora.set_etsi_duty_cycle(True)

# lora.send_ascii('Hello')
# lora.read_n_times(25)

# lora.get_rx_delay()
# lora.set_rx_delay('RX1', 1000)

print("Setup - Start")

lora.set_id('DevEui', '<Your DEVUI>')
lora.set_id('DevAddr', 'Your DEVADDR')
lora.set_key('NWKSKEY', '<Your NWKSKEY>')
lora.set_key('APPSKEY', '<Your APPSKEY>')

lora.set_port(1)
lora.set_dr_band('EU868')
lora.set_mode('LWABP')
lora.set_dr(5)
lora.enable_channel(0)
lora.enable_channel(1)
lora.enable_channel(2)
lora.get_enabled_channels()
lora.set_counters(0, 0) #Comment this line after first firing up your device
lora.set_etsi_duty_cycle(True)


print("Setup - End")
lora.check_link()

time.sleep(4)
cycle = 0
while True:
    print("While cycle: " + str(cycle))
    
    #Send the temperature message
    lora.send_ascii(f"\"TMP:{tmp_sensor.temperature}C\"")
    #Wait for message in downlink if there is any
    msg = lora.wait_for_rx_message(10000)
    
    #If there is a message in the downlink, process it.
    if msg != None:
        print(f"Received Message: {msg} Len: {len(msg)}")
        '''
            ENTER YOUR CODE HERE
        '''
        
    #if cycle == 1:
    #lora.check_link() #If there is an error - Error 0 uncomment this line.
    cycle += 1
    
    #After the transmission, go to sleep for 30 seconds.
    lora.send_raw_command("AT+LOWPOWER")
    response = lora.read_data()
    
    #Check if succesfuly in sleep
    if "SLEEP" in response:
        print("Going to sleep, Bye!")
    
    #Wait until the modem wakes up.
    sleep_ctr = 0
    while sleep_ctr < 30:
        print(f"Time until wakeup: {30-sleep_ctr}")
        time.sleep(1)
        sleep_ctr+=1
    '''while not "WAKE" in response:
        print(f"Time until wakeup: {30-sleep_ctr-sleep_ctr*0.2}")
        time.sleep(1)
        sleep_ctr+=1;
        response = lora.read_data()
        if sleep_ctr > 30:
            break
    '''
    lora.send_raw_command("\n")
    response = lora.read_data()
    print("Wakey wakey!")
    
    
