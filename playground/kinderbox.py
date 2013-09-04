import sys
import os
import serial
import time
import string
import subprocess
import re
import RPi.GPIO as GPIO ## Import GPIO library
import config

PREV = config.PREV
NEXT = config.NEXT
VOLUP = config.VOLUP
VOLDOWN = config.VOLDOWN
TOGGLE = config.TOGGLE

GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(PREV, GPIO.IN)
GPIO.setup(NEXT, GPIO.IN)
GPIO.setup(VOLUP, GPIO.IN)
GPIO.setup(VOLDOWN, GPIO.IN)
GPIO.setup(TOGGLE, GPIO.IN)



class Kinderbox4Kids:

    def __init__(self):
        self.playlist_dir =  config.playlist_dir
        self.rfid_map_file = config.rfid_map_file
        self.track_count = 0
        self.current_track = 1
        self.play_status = 0
        self.is_sleep_mode = False
        self.last_activity_check_ms = 0.0
        self.last_activity_ms = 0.0
        self.sleep_mode_ms = 0.0
        self.go_sleep_mode_time_out = 600
        self.go_standby_mode_time_out = 7200
        #self.power_off_amp_time_out = 120
        self.power_off_amp_time_out = 30
        self.rfid_map = []


    def load_rfid_map(self):
        print "loading %s" % self.rfid_map_file
        if not os.path.exists(self.rfid_map_file):
            print "could not open %s" % self.rfid_map_file
            return
        self.rfid_map = []
        for line in open(self.rfid_map_file, 'r'):
            data = line.strip()
            if len(data) > 0:
                index = data.find('=')
                if index > 0:
                    rfid = data[0:index]
                    barcode = data[index+1:]
                    self.rfid_map.append((rfid, barcode))

    def get_barcode_by_rfid(self, rfid):
        for (rf,bc) in self.rfid_map:
            if rfid == rf:
                return bc
        return

    def load_playlist(self, pls):
        pls_file = os.path.join(self.playlist_dir, "%s.m3u" % pls)
        #print pls_file
        if os.path.exists(pls_file):
            print "loading playlist: %s" % pls
            os.system("mpc stop")
            os.system("mpc clear")
            os.system("mpc load %s" % pls)
            self.track_count = self.get_track_count()
            self.current_track = 1
            if self.track_count > 0:
                os.system("mpc play 1")
        else:
            print "playlist not found!"

    def get_play_status(self):
        process = subprocess.Popen(['mpc'], shell=True, stdout=subprocess.PIPE)
        (st, er) = process.communicate()
        self.track_count = 0
        self.current_track = 0
        self.play_status = 0

        try:
            found = re.findall('\[(.*?)\]', st)
            if len(found) > 0:
                if found[0] == 'paused':
                    self.play_status = 1
                else:
                    # playing
                    self.play_status = 2
            found = re.findall('#(.*?)/', st)
            if len(found) > 0:
                self.current_track = int(found[0].strip())
                #print "current_track = %d" % self.current_track
            found = re.findall('#.*/(.*?)\s\s', st)
            if len(found) > 0:
                self.track_count = int(found[0].strip())
                #print "track count = %d" % self.track_count
        except ValueError, ex:
            print '"%s" cannot be converted to an int: %s' % (found[0], ex)

    def get_track_count(self):
        process = subprocess.Popen(['mpc playlist | wc -l'], shell=True, stdout=subprocess.PIPE)
        (st, er) = process.communicate()
        tcount = 0
        try:
            tcount = int(st.strip())
        except ValueError, ex:
            print '"%s" cannot be converted to an int: %s' % (st, ex)
        return tcount

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

    def process_button(self, button):
        #if self.track_count == 0:
        #    self.track_count = self.get_track_count()
        #    if self.track_count > 0:
        #        self.current_track = 1

        # TOGGLE
        #if button == '0':
        #    print "on/off"
        #    if not self.is_sleep_mode:
        #        self.go_sleep()
        #    else:
        #        self.go_wakeup()

        # ignore other buttons if in sleep mode
        #if self.is_sleep_mode:
        #    return

        # PREV
        if button == 'PREV':
            if self.current_track > 1:
                self.current_track = self.current_track - 1
                os.system("mpc play %d " % self.current_track)
            else:
                print "Current track is minumum"

        # PLAY/PAUSE
        if button == 'TOGGLE':
            os.system("mpc toggle")

        #NEXT
        if button == 'NEXT':
            if self.current_track < self.track_count:
                self.current_track = self.current_track + 1
                os.system("mpc play %d " % self.current_track)
            else:
                print "Current track is minumum"

        #VOLUME UP
        if button == "VOLUP":
            os.system("mpc volume +5")

        #VOLUME DOWN
        if button == "VOLDOWN":
            os.system("mpc volume -5")

    def run(self):
        self.load_rfid_map()
        print "connect to serial ..."       
        ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.1)
        print("connected")
        ser.open()
        ser.write("testing")
        current_barcode = ""
        print "Huy Testing"
        prev_input = None
        last_ms = time.time()
        try:
            while 1:
                #Read button state
                input =  None
                if(GPIO.input(PREV)):
                    input = "PREV"
                if(GPIO.input(NEXT)):
                    input = "NEXT"
                if(GPIO.input(VOLUP)):
                    input = "VOLUP"
                if(GPIO.input(VOLDOWN)):
                    input = "VOLDOWN"
                if(GPIO.input(TOGGLE)):
                    input = "TOGGLE"
                if ((not prev_input) and input):
                    self.process_button(input)
                prev_input = input
                #Read rfid card
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
                        decimalData = self.tag_to_dec(rawData)
                        print "RFID Reading = %s" % decimalData
                        barcode = self.get_barcode_by_rfid(str(decimalData))
                        if barcode is None:
                            print "Album not existed..."
                        else:
                            if current_barcode != barcode:
                                current_barcode = barcode
                                self.load_playlist(barcode)
                time.sleep(0.1)
                current_ms = time.time()

                #Update display each  0.5ms:
                if (current_ms - last_ms) > 2:
                    last_ms = current_ms
                    self.get_play_status()
        except KeyboardInterrupt:
            ser.close()
        ser.close()


Kinderbox4Kids().run()
