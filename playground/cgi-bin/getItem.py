#!/usr/bin/env python
import cgitb
import os, json, sys
import config
sys.path.append('/home/pi/db')
import DBModule
cgitb.enable()

db = DBModule.DBUtils()

def run():
    listItem = db.get_all_item()
    item_map = []
    for (r, b, n) in listItem:
        rfid = r
        barcodeid = b
        name = n
        d = dict(rfid = rfid, barcode = barcodeid, name = name)
        item_map.append(d)
    js = json.dumps({"data": item_map})
    print js

print "Content-Type: application/json;charset=UTF-8"
print
run()


