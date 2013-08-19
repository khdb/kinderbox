import sys
import os
import serial
import time
import string
import subprocess
import re


class Jukebox4Kids:

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

    def run(self):
        self.load_rfid_map()
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
				print "Get buffer from serial...."
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
							decimalData += str(ord(d))
				if len(decimalData) > 0 and len(rawData) > 0:
					print "Finish get buffer"
					print "\tRaw Data =  %s" % rawData
					print "\tDecimal Data = %s" % decimalData
				if decimalData == "706948485456574970497054":
					os.system("mpc play 1")
				elif decimalData == "496848485652666857546650":
					os.system("mpc play 3")
							
	except KeyboardInterrupt:
		ser.close()


Jukebox4Kids().run()
