#!/usr/bin/env python
import cgitb
import os, signal,sys
import config, time
import serial
import LoggerModule
import LCDModule
sys.path.append("/home/pi/db")
import DBModule

#cgitb.enable()

db = DBModule.DBUtils()
lcd = LCDModule.LCD()

def char_to_hex(cdata):
    return {
            '0': 0x00,
            '1': 0x01,
            '2': 0x02,
            '3': 0x03,
            '4': 0x04,
            '5': 0x05,
            '6': 0x06,
            '7': 0x07,
            '8': 0x08,
            '9': 0x09,
            'A': 0x0A,
            'B': 0x0B,
            'C': 0x0C,
            'D': 0x0D,
            'E': 0x0E,
            'F': 0x0F,
            'a': 0x0A,
            'b': 0x0B,
            'c': 0x0C,
            'd': 0x0D,
            'e': 0x0E,
            'f': 0x0F,
            }[cdata]

def tag_to_dec(rawData):
    rfid = 0
    for idx, r in enumerate(rawData):
        if idx >= 2 and idx <= 9:
            hdata = char_to_hex(r)
            rfid =  rfid | hdata
            if idx < 9:
                rfid = rfid << 4
    return rfid


def add_rfid( rfid):
    if db.check_rfid_existed(rfid):
        #RFID is existed!!
        cmd = "curl http://localhost:9292/faye -d 'message={\"channel\":\"/messages/new\", \"data\":\"%s-duplicate\"}'" %rfid
        os.system(cmd)
    else:
        db.insert_free_rfid(rfid)
        send_notification(rfid)

def send_notification(rfid):
    cmd = "curl http://localhost:9292/faye -d 'message={\"channel\":\"/messages/new\", \"data\":\"%s\"}'" %rfid
    os.system(cmd)
    time.sleep(1)


def reading_rfid():
    ser = serial.Serial('/dev/ttyAMA0',9600, timeout=1)
    ser.open()
    lcd.message("Kinderbox stopped", "Ready to add new card")
    try:
        while 1:
            rawData = []
            decimalData = ""
            isRead = False
            buf = ser.read(100)
            if len(buf) > 0:
                for d in buf:
                    if d == '\x02':
                        rawData = []
                        isRead = True
                    elif d == '\x03':
                        isRead = False
                        break
                    else:
                        if isRead:
                            rawData.append(d)
                if len(rawData) > 0:
                    decimalData = str(tag_to_dec(rawData))
                    print "RFID Reading = %s" % decimalData
                    add_rfid(str(decimalData))
    except Exception, ex:
        logger = LoggerModule.Logger("Reading RFID")
        logger.error("%s" %ex)
    finally:
        lcd.turn_off()
        ser.close()


def main():
    reading_rfid()


if __name__ == "__main__":
   main()

