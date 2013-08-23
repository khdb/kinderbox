import serial
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
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
except KeyboardInterrupt:
        ser.close()



