import os
import time
from smbus import SMBus
#from RPi import GPIO

addr = 0x48
channel = 0b1000010
bus = SMBus(1)


while(1):
    os.system('clear')

    bus.write_byte(addr, channel)
    bus.read_byte(addr)
    value = bus.read_byte(addr)

    print(255-value)
    time.sleep(0.1)

