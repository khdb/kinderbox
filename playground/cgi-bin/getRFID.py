#!/usr/bin/env python
import cgitb
import os, json, sys
import config
sys.path.append('/home/pi/db')
import DBModule
cgitb.enable()

db = DBModule.DBUtils()

def run():
    rfid_list = db.get_all_rfid()
    js = json.dumps({"data": rfid_list})
    print js

print "Content-Type: application/json;charset=UTF-8"
print
run()
