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
    except Exception, ex:
        logger = LoggerModule.Logger("Mapping RFID with Album")
        logger.error("%s" %ex)
        print "Have error: %s" %ex


print "Content-Type: application/json;charset=UTF-8"
print
run()
