#!/usr/bin/python
 
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import LoggerModule

class LCD:

    __line1 = ""
    __line2 = ""
    __message = ""
    def __init__(self):
        self.lcd = Adafruit_CharLCD()
        self.lcd.clear()
        self.logger = LoggerModule.Logger()

    def hello(self):
        self.lcd.message("  Welcome to \n Kinderbox ")

    def turn_off(self):
        self.lcd.noDisplay()

    def display_pause(self):
        self.message("", "Pause")

    def display_ready(self):
        self.message("", "Ready")


    def message(self, line1, line2):
        if self.__line1 == line1 and self.__line2 == line2:
                return
        self.lcd.clear()
        sleep(0.5)
        self.lcd.message(line1 + "\n" + line2)
        self.__line1 = line1
        self.__line2 = line2

    def scroll_to_left(self):
        #Check size message. If over 16 character --> move
        if len(self.__line1) > 16 or len(self.__line2) > 16:
            self.lcd.DisplayLeft()


