#!/usr/bin/env python
import cgitb, cgi
import os, json, sys
import config
sys.path.append('/home/pi/db')
import DBModule
cgitb.enable()

db = DBModule.DBUtils()

def run():
    try:
        data = sys.stdin.read()
        d = json.loads(data)
        barcodeid = d['barcodeid']
        if barcodeid is None:
            js = json.dumps({"result":"error. barcodeid is None"})
        else:
            db.delete_item_by_barcodeid(barcodeid)
            js = json.dumps({"result":"success"})
    except Exception, ex:
        js = json.dumps({"result":"error: %s" %ex})
    finally:
        print js


print "Content-Type: application/json;charset=UTF-8"
print
run()
