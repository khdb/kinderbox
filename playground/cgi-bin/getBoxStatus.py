#!/usr/bin/env python
import cgitb
import os, json, sys
import subprocess, re, traceback
import config
import LoggerModule
cgitb.enable()

logger = LoggerModule.Logger("Get box status")
main = "/home/pi/huy-projects/kinderbox/"
api = "/var/www/cgi-bin/"

def check_python_process(name):
    try:
        process = subprocess.Popen(['ps aux | grep "%s"' %name], shell=True, stdout=subprocess.PIPE)
        (st, er) = process.communicate()

        l = []
        l.append("python.*")
        l.append("[%s]" %name)
        #l.append(".*%")

        pattern = ''.join(l)
        found = re.findall(pattern, st)
        if len(found) > 0:
            return "on"
        else:
            return "off"
    except Exception, ex:
        logger.error("%s" %ex)
        return "unknown"

def run():
    try:
        is_reading = check_python_process("readingRFID.py")
        is_kinderbox = check_python_process("kinderbox.py")
        d = dict(ScanNewRFID = is_reading, Kinderbox = is_kinderbox)
        js = json.dumps({"data": d})
    except Exception, ex:
        logger.error("%s" %ex)
        js = json.dumps({"error": "%s" %ex})
    finally:
        print js

print "Content-Type: application/json;charset=UTF-8"
print
run()


