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
        print "could not open %s" % rfid_map_file
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

def delete_rfid_map(rfid_map, rfid):
    for  index, item in enumerate(rfid_map):
        if (item[0] == rfid):
            save_to_file(rfid_map, rfid)
            return
    print "Error: RFID is not existed in database"
def save_to_file(rfid_map, rfid):
    f = open(config.rfid_map_file, 'w')
    for (rf, bc, name) in rfid_map:
        if (rf == rfid):
            continue
        if bc:
            entry = "%s=%s=%s\n" % (rf,bc,name)
        else:
            entry = "%s\n" % rf
        f.write(entry)
    f.close()
    print "Delete success"


def checkInputData():
    arguments = cgi.FieldStorage()
    for i in arguments.keys():
        if i == "rfid":
            rfid = str(arguments[i].value)
    if (rfid is None):
        print "Missing parameter..."
    else:
        rfid_map = load_rfid_map()
        delete_rfid_map(rfid_map, rfid)

checkInputData()
