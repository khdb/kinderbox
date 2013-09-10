import sys, os, serial

class Sensor:
    ser = None

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.1)

    def open(self):
        self.ser.open()

    def close(self):
        self.ser.close()

    def char_to_hex(self, cdata):
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

    def tag_to_dec(self, rawData):
        rfid = 0
        for idx, r in enumerate(rawData):
                if idx >= 2 and idx <= 9:
                        hdata = self.char_to_hex(r)
                        rfid =  rfid | hdata
                        if idx < 9:
                                rfid = rfid << 4
        return rfid

    def get_rfid_code(self):
        rawData = []
        decimalData = ""
        isRead = False
        buf = self.ser.read(100)
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
                decimalData = self.tag_to_dec(rawData)
                print "RFID Reading = %s" % decimalData
                return str(decimalData)
        return None
