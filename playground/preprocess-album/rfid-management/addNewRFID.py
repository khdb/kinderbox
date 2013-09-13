import os, sys
import serial
sys.path.append("/home/pi/db")
import DBModule

db = DBModule.DBUtils()



def saveRFID(rfid):
    if db.check_rfid_existed(rfid):
        print "Not save! RFID = %s is existed!" % rfid
    else:
        print "Saving RFID = %s..." % rfid
        db.insert_free_rfid(rfid)

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


def main(argv):
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
    ser.open()
    ser.write("testing")
    print "Ready to receive RFID card:"
    try:
        while 1:
            parse_data = False
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
                print "\n------------------------------------------\n"
                decimalData = tag_to_dec(rawData)
                print "RFID  = %s" % decimalData
                saveRFID(str(decimalData))
    except KeyboardInterrupt:
        ser.close()
    finally:
        ser.close()

if __name__ == "__main__":
    main(sys.argv[1:])
