#!/usr/bin/env python

import os
import datetime
import sqlite3
import serial
import I2C_LCD_driver
import time
import atexit

#from datetime import datetime
#from time import  strftime time sleep
#from interruption import *
import threading
import wiringpi
import RPi.GPIO as GPIO
GPIO.setmode (GPIO.BOARD) 
#from gpio import digital_write
#from gpio import digital_read
#from gpio import pin_mode
#from gpio import pin_mode
#from adc import analog_read
#from pyduino_pcduino import *

from mpr121 import *
import ephem
import math
import wget
from Tkinter import * 
import itertools
import bme280



from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey,Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from pytz import utc
Base = declarative_base()
metadata = MetaData()

def delay(ms):
	time.sleep(1.0*ms/1000)


keyboard0=mpr121setup(0x5a)
while (1):
	delay (200)
	touchdata= mpr121readData(0x5a)
	if touchdata != 0 :
		print (str(touchdata))
		inter_state1 = touchdata
	


