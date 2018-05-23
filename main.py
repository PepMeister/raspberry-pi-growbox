#coding:UTF8
import os
import time
import datetime
import logging

from smbus import SMBus
from RPi import GPIO
from threading import Thread

logging.basicConfig(filename="growbox.log", level=logging.INFO)

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT) # управление освещением
GPIO.setup(9, GPIO.OUT) # управление поливом



def watering(watering_time):
	wet_level = 200 # выставляем уровень влажности почвы, который необходимо достичь при поливе

	watering.next_wat = datetime.datetime.now().day+watering_time['interval']

	addr = 0x48
	channel = 0b1000010
	bus = SMBus(1)

	while(True):
		if (watering.next_wat.day == datetime.datetime.now().day and watering_time['acthour'] == datetime.datetime.now().hour):
			watering.next_wat = datetime.datetime.now().day+watering_time['interval']

			bus.write_byte(addr, channel)
			value = bus.read_byte(addr)

			if 255-value == 0:			 # начинаем полив только если земля полностью сухая
			logging.info("watering is on")
				while(255-value < wet_level):

					GPIO.output(9, True) # включаем помпу на 3 секунды
					time.sleep(3)
					GPIO.output(9, False)# выключаем
					time.sleep(10)		 # ждем пока вода впитается в землю
					value = bus.read_byte(addr) # считываем данные с модуля влажности почвы
			logging.info("watering is off")
			else:
				logging.warning("the plant is already watered")
		time.sleep(1*60)


def lighting(lighting_time):
	while(True):
		if (datetime.datetime.now().hour == lighting_time['acthour']):
			GPIO.output(10, True)
			logging.info("lighting is on, time: ",datetime.datetime.now())
		if (datetime.datetime.now().hour == lighting_time['offhour']):
			GPIO.output(10, False)
			logging.info("lighting is off, time:",datetime.datetime.now())
		time.sleep(1*60)


def main():
	watering_time = {'interval':7, 'acthour':12}
	lighting_time = {'acthour':11, 'offhour':23}

	W = Thread(target=watering, args=(watering_time,))
	L = Thread(target=lighting, args=(lighting_time,))

	W.start()
	L.start()


if __name__ == "__main__":
	main()
