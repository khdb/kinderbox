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
        listItem = db.get_all_item()
        item_map = []
        if listItem is None:
            print json.dumps({"data": item_map})
            return
        for (r, b, n, cr) in listItem:
            rfid = r
            barcodeid = b
            name = n
            created_date = cr 
            d = dict(rfid = rfid, barcodeid = barcodeid, name = name, created_at = created_date)
            item_map.append(d)
        js = json.dumps({"data": item_map})
    except Exception, ex:
        logger = LoggerModule.Logger("Get item")
        logger.error("Get item error: %s" %ex)
        js = json.dumps({"error": "%s" %ex})
    finally:
        print js

print "Content-Type: application/json;charset=UTF-8"
print
run()


