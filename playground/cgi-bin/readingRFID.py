#!/usr/bin/env python
import cgitb
import os, signal
import config, time
import serial

#cgitb.enable()

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

def load_rfid_map():
    if not os.path.exists(config.rfid_map_file):
        print "could not open %s" % config.rfid_map_file
        return
    rfid_map = []
    for line in open(config.rfid_map_file, 'r'):
        data = line.strip()
        if len(data) > 0:
            lstdata = data.split('=')
            if len(lstdata) == 1:
                rfid = data
                barcode = None
                name = None
            else:
                rfid = lstdata[0]
                barcode = lstdata[1]
                if len(lstdata)== 3:
                    name = lstdata[2]
                else:
                    name = None
            rfid_map.append((rfid, barcode, name))
    return  rfid_map

def add_rfid(rfid_map, rfid):
    for rf,bc,name in rfid_map:
        if (rf == rfid):
            #RFID is existed!!
            cmd = "curl http://localhost:9292/faye -d 'message={\"channel\":\"/messages/new\", \"data\":\" hello, RFID number %s is duplicate \"}'" %rfid
            os.system(cmd)
            return rfid_map
    save_rfid(rfid)
    rfid_map.append((rfid, None, None))
    send_notification(rfid)
    return rfid_map

def send_notification(rfid):
    cmd = "curl http://localhost:9292/faye -d 'message={\"channel\":\"/messages/new\", \"data\":\" hello, this is RFID number %s \"}'" %rfid
    os.system(cmd)
    print "cmd = %s" % cmd
    time.sleep(1)

def save_rfid(rfid):
    with open(config.rfid_map_file, 'a') as myfile:
        entry ="%s\n" % rfid
        myfile.write(entry)


def reading_rfid():
    rfid_map = load_rfid_map();
    ser = serial.Serial('/dev/ttyAMA0',9600, timeout=1)
    ser.open()
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
                    rfid_map = add_rfid(rfid_map, decimalData)
    except KeyboardInterrupt:
        ser.close()
    ser.close()


def main():
    reading_rfid()


if __name__ == "__main__":
   main()

