import sys
import serial

rfid_management_file = "/home/pi/huy-projects/kinderbox/playground/preprocess-album/rfid-management/RFID.management"

def loadRFID():
	rfid_map = []
    	for line in open(rfid_management_file, 'r'):
        	data = line.strip()
        	if len(data) > 0:
            		index = data.find('=')
            		if index > 0:
                		rfid = data[0:index]
                		desc = data
                		rfid_map.append((rfid, desc))
			else:
				rfid = data
				desc = "NULL"
				rfid_map.append((rfid, desc))
    	return rfid_map

def saveRFID(rfid, rfid_map):
	if checkRFIDExisted(rfid, rfid_map):
		print "Not save! RFID = %s is existed!" % rfid
	else:
		print "Saving RFID = %s..." % rfid 
		with open(rfid_management_file, "a") as myfile:
			entry = "%s\n" % (rfid)
			myfile.write(entry)
		rfid_map.append((rfid,"NULL"))

def checkRFIDExisted(rfid, rfid_map):
	for (rf, desc) in rfid_map:
		if rfid == rf:
                	return True
        return False

def main(argv):
	rfid_map = loadRFID()
	ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
	ser.open()
	ser.write("testing")
	print "Ready to receive RFID card:"
	try:
        	while 1:
			parse_data = False
			decimalData = ""
			isRead = False
			buf = ser.read(100)
			if len(buf) > 0:
              			for d in buf:
					if d == '\x02':
						isRead = True
                        		elif d == '\x03':				
						isRead = False
						break
                             		else:
						if isRead:
							decimalData += str(ord(d))
			if len(decimalData) > 0:
				print "\n------------------------------------------\n"
				print "RFID  = %s" % decimalData
				saveRFID(decimalData, rfid_map)
	except KeyboardInterrupt:
        	ser.close()

if __name__ == "__main__":
	main(sys.argv[1:])
