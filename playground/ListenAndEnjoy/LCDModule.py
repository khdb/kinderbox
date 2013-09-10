#!/usr/bin/python
 
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
 
#lcd = Adafruit_CharLCD()
#cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
#lcd.begin(16,1)

class LCD:

    def __init__(self):
        self.lcd = Adafruit_CharLCD()
        self.lcd.clear()

    def hello(self):
        self.lcd.message("  Welcome to \n Kinderbox ")

    def turn_off(self):
        self.lcd.noDisplay()

    def message(self, message):
        self.lcd.clear()
        self.lcd.message(message)
