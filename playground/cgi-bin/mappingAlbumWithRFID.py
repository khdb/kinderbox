#!/usr/bin/env python
import cgitb
import os, json, sys
import config
sys.path.append('/home/pi/db')
import DBModule
cgitb.enable()

db = DBModule.DBUtils()

def run():
    free_rfid =  db.get_free_rfid()
    while (free_rfid):
        free_album = db.get_free_album()
        if free_album is None:
            break
        barcodeid = free_album[1]
        name = free_album[2]
        db.update_item_by_barcodeid(free_rfid[0], barcodeid, name)
        free_rfid = db.get_free_rfid()
    print "Mapping done"

print "Content-Type: application/json;charset=UTF-8"
print
run()
