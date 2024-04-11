import machine
import time

led = machine.Pin(15, machine.Pin.OUT)
led.value(0)

while(1):
    led.toggle()
    print(time.ticks_ms())
    time.sleep(1)