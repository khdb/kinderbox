import sys, os

rfid_management_file = "/home/pi/huy-projects/kinderbox/playground/preprocess-album/rfid-management/RFID.management"

def loadRFID():
	rfid_map = []
    	for line in open(rfid_management_file, 'r'):
        	data = line.strip()
        	if len(data) > 0:
			lststr = data.split('=')
            		if len(lststr) == 1:
                		rfid = data
				barcodeid = None
				desc = None
                		rfid_map.append((rfid, barcodeid, desc))
			else:
				rfid = lststr[0]
				barcodeid = lststr[1]
				desc = lststr[2] 
				rfid_map.append((rfid, barcodeid, desc))
    	return rfid_map

def get_rfid_by_barcode(barcodeid, rfid_map):
	for (rf, bc, desc) in rfid_map:
        	if barcodeid  == bc:
                	return rf
        return

def get_new_rfid(rfid_map):
	for (rf, bc, desc) in rfid_map:
		if bc is None:
			return rf
	return
	
def save_rfid_file(rfid_path, rfid):
	with open(rfid_path, "w") as myfile:
		entry = "%s" % (rfid)
		myfile.write(entry)

def update_barcode_desc(rfid_map, rfid, barcode, description):
	for index, item in enumerate(rfid_map):
		#print index
		#print item
		if (item[0] == rfid):
			print "ITEM -----"
			#item[1] = barcode
			#item[2] = description
                        rfid_map[index] = rfid, barcode, description
			save_rfid_management(rfid_map)		
			#return
	print "Error: Have problem when update RFID Management... Check rfid = %s" % rfid

def save_rfid_management(rfid_map):
	print "Save RFID Management: "
	print rfid_map
	f = open(rfid_management_file, 'w')
    	for (rfid, barcode, description) in rfid_map:
		if (barcode is None):
			entry = "%s\n" % rfid
		else:
	        	entry = "%s=%s=%s\n" % (rfid, barcode, description)
		print "Entry = %s" % entry
        	f.write(entry)
    	f.close()

def main(argv):
	path = "."
   	if len(argv) > 0:
      		path = argv[0]

	if not os.path.exists(path) and not os.path.isdir(path):
     		print "expecting path!"
      		return   

	idfile = os.path.join(path, 'barcode.id')
	if not os.path.exists(idfile):
		print "Missing Barcode.id file"
		return
	rfid_map = loadRFID();
	barcode_id = str(open(idfile).read()).strip()

	rfid_file = os.path.join(path, 'rfid.id')
	rfid = get_rfid_by_barcode(barcode_id, rfid_map)
	if rfid is None:
		#Get new RFID from RFID Management
		rfid = get_new_rfid(rfid_map)
		if rfid is None:
			print "Error: Not enough free RFID. Please import new RIFD..."
		else:
			save_rfid_file(rfid_file, rfid)
	else:
		#Update RFID
		save_rfid_file(rfid_file, rfid)

	#Update BarcodeID into RFID Management
	update_barcode_desc(rfid_map, rfid, barcode_id, path)


if __name__ == "__main__":
	main(sys.argv[1:])

