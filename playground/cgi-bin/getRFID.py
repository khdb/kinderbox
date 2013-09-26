#!/usr/bin/env python
import cgitb
import os, json, sys
import config
import LoggerModule
sys.path.append('/home/pi/db')
import DBModule
cgitb.enable()

db = DBModule.DBUtils()

def run():
    try:
        rfid_list = db.get_all_rfid()
        js = json.dumps({"data": rfid_list})
    except Exception, ex:
        logger = LoggerModule.Logger("Get all RFID")
        logger.error("Get RFID error: %s" %ex)
        js = json.dumps({"error": "%s" %ex})
    finally:
        print js


print "Content-Type: application/json;charset=UTF-8"
print
run()
