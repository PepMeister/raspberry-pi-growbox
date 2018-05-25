#coding:UTF8
import os
import time
import datetime
import logging
import atexit

from smbus import SMBus
from RPi import GPIO
from threading import Thread

logging.basicConfig(filename="growbox.log", level=logging.INFO)

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT) # управление освещением
GPIO.setup(9, GPIO.OUT) # управление поливом



def sendmessage(er_num):
	pass


def watering(watering_time):
	wet_level = 200 # выставляем уровень влажности почвы, который необходимо достичь при поливе
	watering.output = False

	addr = 0x48
	channel = 0b1000010
	bus = SMBus(1)
	#datetime.datetime.today().weekday()

	while(True):
		if (datetime.datetime.now().weekday() == watering_time['weekday'] and datetime.datetime.now().hour == watering_time['acthour']) and watering.output == False:

			watering.output = True
			bus.write_byte(addr, channel)
			value = bus.read_byte(addr)

			if 255-value == 0:			 # начинаем полив только если земля полностью сухая
				logging.info("watering is on")
				с = 0
				while(255-value < wet_level):
					if c==3 and 255-value==0:
						sendmessage(1)
					GPIO.output(9, True) # включаем помпу на 3 секунды
					time.sleep(3)
					GPIO.output(9, False)# выключаем
					time.sleep(10)		 # ждем пока вода впитается в землю
					value = bus.read_byte(addr) # считываем данные с модуля влажности почвы
					c+=1
				logging.info("watering is off")
				sendmessage(0)
			else:
				logging.warning("the plant is already watered")
				sendmessage(2)
		if  not (watering_time['acthour'] == datetime.datetime.now().hour):
			watering.output = False
		time.sleep(1*60*10)


def lighting(lighting_time):
	lighting.output = False #
	while(True):
		if (datetime.datetime.now().hour >= lighting_time['acthour']) and (datetime.datetime.now().hour < lighting_time['offhour']) and lighting.output == False:
			GPIO.output(10, True)
			logging.info("lighting is on")
			lighting.output = True
		if datetime.datetime.now().hour >= lighting_time['offhour'] and datetime.datetime.now().hour < 24 and lighting.output == True or datetime.datetime.now()$
			GPIO.output(10, False)
			logging.info("lighting is off")
			lighting.output = False
		time.sleep(1*60)


@atexit.register
def exit_func():
	logging.info("--the program is stopped--, time: "+str(datetime.datetime.now()))
	GPIO.cleanup()


def main():
	logging.info("--the program is started--, time:"+str(datetime.datetime.now()))
	watering_time = {'weekday':5, 'acthour':12} #день недели (0-понедельник, 6-воскресенье)
	lighting_time = {'acthour':11, 'offhour':23}

	W = Thread(target=watering, args=(watering_time,))
	L = Thread(target=lighting, args=(lighting_time,))

	W.start()
	L.start()


if __name__ == "__main__":
	main()
