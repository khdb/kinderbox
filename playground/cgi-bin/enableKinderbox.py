#!/usr/bin/env python
import cgitb
import os, signal
import config
import LoggerModule
cgitb.enable()

def kill_all_python():
    cmd = "sudo killall python"
    os.system(cmd)

def kill_kinderbox():
    cmd = "sudo pkill -9 -f kinderbox.py"
    os.system(cmd)

def kill_reading_RFID():
    cmd = "sudo pkill -9 -f readingRFID.py"
    os.system(cmd)


def stop_mpc():
    cmd = "mpc stop"
    os.system(cmd)

def main():
    try:
        #Kill all python and mpc
        kill_kinderbox()
        kill_reading_RFID()
        #Run readingRFID.py : receive new RFID from sensor
        os.system("sudo python /home/pi/huy-projects/kinderbox/kinderbox.py &")
        print "Status: 204 NO CONTENT"
        print "Content-Type: application/json;charset=UTF-8"
        print
    except Exception, e:
        logger = LoggerModule.Logger("Enable Kinderbox")
        logger.error("%s" %e)
        print "Status: 400 BAD REQUEST"
        print "Content-Type: application/json;charset=UTF-8"
        print
        print "Unexpected error: %s" % e

if __name__ == "__main__":
   main()

