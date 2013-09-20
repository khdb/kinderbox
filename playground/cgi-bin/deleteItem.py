#!/usr/bin/env python
import cgitb, cgi
import os, json, sys, shutil
import config
sys.path.append('/home/pi/db')
import DBModule
cgitb.enable()

music_path = "/var/lib/mpd/music/"
playlist_path = "/var/lib/mpd/playlists/"
db = DBModule.DBUtils()

def remove(path):
    if os.path.exists(path):
        cmd = 'rm -rf "%s"' %path
        os.system(cmd)

def run():
    try:
        data = sys.stdin.read()
        d = json.loads(data)
        barcodeid = d['barcodeid']
        if barcodeid is None:
            js = json.dumps({"result":"error. barcodeid is None"})
        else:
            item = db.get_item_by_barcodeid(barcodeid)
            if item is None:
                js = json.dumps({"result":"error. Album not existed"})
                return
            name = item[2]
            #Delete database
            db.delete_item_by_barcodeid(barcodeid)
            #Delete m3u
            m3u_file = os.path.join(playlist_path, "%s.m3u" %barcodeid)
            remove(m3u_file)
            #Delete datafile
            music_dir = os.path.join(music_path,name)
            remove(music_dir)

            js = json.dumps({"result":"success"})
    except Exception, ex:
        js = json.dumps({"result":"error: %s" %ex})
    finally:
        print js


print "Content-Type: application/json;charset=UTF-8"
print
run()
