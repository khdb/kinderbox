#!/usr/bin/python
 
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, strftime
import LoggerModule
import normalization

class LCD:

    __line1 = ""
    __line2 = ""
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
        try:
            n_line1 = normalization.remove_unicode(line1)
        except:
            n_line1 = "unkown"
        try:
            n_line2 = normalization.remove_unicode(line2)
        except:
            n_line2 = "unkown"

        self.lcd.clear()
        sleep(0.5)
        message = "%s\n%s" %(n_line1,n_line2)
        print "Message: %s" %(message)
        self.lcd.message(message)
        self.__line1 = line1
        self.__line2 = line2

    def scroll_to_left(self):
        #Check size message. If over 16 character --> move
        if len(self.__line1) > 16 or len(self.__line2) > 16:
            self.lcd.DisplayLeft()


