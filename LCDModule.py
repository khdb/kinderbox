#!/usr/bin/python
 
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, strftime, time
from subprocess import *
import LoggerModule
import normalization

class LCD:

    __line1 = ""
    __line2 = ""
    __isLock = False
    __wait = 3 #seconds
    def __init__(self):
        self.lcd = Adafruit_CharLCD()
        self.lcd.clear()
        self.logger = LoggerModule.Logger("LCD Module")

    def hello(self):
        self.lcd.message("  Welcome to \n Kinderbox ")

    def turn_off(self):
        self.lcd.noDisplay()

    def display_ip(self):
        cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
        p = Popen(cmd, shell=True, stdout=PIPE)
        ipaddr = p.communicate()[0]
        self.message("Ready to scan", "IP: %s" %ipaddr, True)

    def display_pause(self):
        self.message("", "Pause", True)

    def display_ready(self):
        #self.message("", "Ready", True)
        self.display_ip()

    def display_volume(self, message):
        self.message("", message, True)
        self.__isLock = True
        self.__locked_time = time()


    def message(self, line1, line2, force = False):
        if force:
            self.__isLock = False

        if self.__isLock:
            current_time = time()
            if current_time - self.__locked_time >= self.__wait:
                self.__isLock == False
            else:
                return

        if self.__line1 == line1 and self.__line2 == line2:
            return

        try:
            n_line1 = normalization.remove_unicode(line1)
        except Exception, e1:
            print "Line1: %s" %e1
            n_line1 = "unkown"

        try:
            n_line2 = normalization.remove_unicode(line2)
        except Exception, e2:
            print "Line2: %s" %e2
            n_line2 = "unkown"

        self.lcd.clear()
        sleep(0.5)
        message = "%s\n%s" %(n_line1,n_line2)
        self.lcd.message(message)
        self.__line1 = line1
        self.__line2 = line2

    def scroll_to_left(self):
        #Check size message. If over 16 character --> move
        if len(self.__line1) > 16 or len(self.__line2) > 16:
            self.lcd.DisplayLeft()


