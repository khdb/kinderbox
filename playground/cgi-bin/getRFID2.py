#!/usr/bin/env python
import cgitb
import os, json
import config

cgitb.enable()

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
                d = dict(rfid = rfid, barcode = barcode, name = name)
                rfid_map.append(d)
        #js = json.dumps(rfid_map)
        js = json.dumps({"data" : rfid_map})
        print js
        #print "JSON_CALLBACK(" + js + ")"

#print "Content-Type: application/json;charset=UTF-8"
print "Header: Access-Control-Allow-Origin: *"
#print "Content-Type: application/javascript;charset=UTF-8"
print "Content-Type: application/json;charset=UTF-8"
print
load_rfid_map()


