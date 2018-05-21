#coding:UTF8
import os
import time
import datetime

from smbus import SMBus
from RPi import GPIO
from threading import Threading

addr = 0x48
channel = 0b1000010
bus = SMBus(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT) # управление освещением
GPIO.setup(9, GPIO.OUT) # управление поливом


def watering():
	while(True):
		os.system('clear')

        bus.write_byte(addr, channel)
        bus.read_byte(addr)
        value = bus.read_byte(addr)

        print(255-value)
        time.sleep(0.1)


def lighting(lighting_time):
	while(True):
		T = datetime.datetime.now()
		if (T.hour == lighting_time['acthour']):
			GPIO.output(10, True)
		if (T.hour == lighting_time['offhour']):
			GPIO.output(10, False)
		time.sleep(1*60)



def main():
	#watering_time
	lighting_time = {'acthour':11, 'offhour':23}

	#W = Threading(target=watering, args=(watering_time,))
	L = Threading(target=lighting, args=(lighting_time,))

	#W.start()
	L.start()

	#GPIO.cleanup()

if __name__ == "__main__":
	main()