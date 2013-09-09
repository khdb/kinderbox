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

def add_rfid_map(rfid_map, rfid):
    for  index, item in enumerate(rfid_map):
        if (item[0] == rfid):
            print "Error: RFID is existed in database"
            return
    with open(config.rfid_map_file, 'a') as myfile:
        entry = "%s\n" % rfid
        myfile.write(entry)
    print "Add success"

def checkInputData():
    arguments = cgi.FieldStorage()
    rfid = None
    path = None
    for i in arguments.keys():
        if i == "rfid":
            rfid = str(arguments[i].value)
        if i == "path":
            path = str(arguments[i].value)
    if (rfid is None) or (path is None):
        print "Missing parameter..."
    else:
        print path
        #downloadAlbum(album)
        #rfid_map = load_rfid_map()
        #add_rfid_map(rfid_map, rfid)

checkInputData()
