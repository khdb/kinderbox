#!/usr/bin/env python
import cgitb
import sys
import os, json
import cgi
import config

cgitb.enable()

print "Content-Type: text/html;charset=UTF-8"
print

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
    return rfid_map

def set_rfid_map(rfid_map, rfid, barcode, name):
    for  index, item in enumerate(rfid_map):
        if (item[0] == rfid):
            rfid_map[index] = rfid, barcode, name
            save_to_file(rfid_map)
            return
    print "Error: RFID not found in database"

def save_to_file(rfid_map):
    f = open(config.rfid_map_file, 'w')
    for (rf, bc, name) in rfid_map:
        if bc:
            entry = "%s=%s=%s\n" % (rf,bc,name)
        else:
            entry = "%s\n" % rf
        f.write(entry)
    f.close()
    print "Save success"

def checkInputData():
    arguments = cgi.FieldStorage()
    for i in arguments.keys():
        if i == "rfid":
            rfid = str(arguments[i].value)
        if i == "barcode":
            barcode = str(arguments[i].value)
        if i == "name":
            name = arguments[i].value
    if (rfid is None) or (barcode is None) or (name is None):
        print "Missing parameter..."
    else:
        rfid_map = load_rfid_map()
        set_rfid_map(rfid_map, rfid, barcode, name)

checkInputData()
