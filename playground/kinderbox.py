import sys
import os
import serial
import time
import string
import subprocess
import re


class Kinderbox4Kids:

    def __init__(self):
        self.playlist_dir = "/var/lib/mpd/playlists"
        self.rfid_map_file = "/home/pi/huy-projects/kinderbox/playground/rfidmap.properties"
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


    def run(self):
        self.load_rfid_map()
				print self.rfid_map
        print "connect to serial ..."       
        ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
        print("connected")
				ser.open()
				ser.write("testing")
				print "Huy Testing"
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
					decimalData = self.tag_to_dec(rawData)
					print "RFID Reading = %s" % decimalData
					barcode = self.get_barcode_by_rfid(str(decimalData))
					if barcode is None:
						print "Album not existed..."
					else:
						self.load_playlist(barcode)
			
		except KeyboardInterrupt:
		ser.close()


Kinderbox4Kids().run()
