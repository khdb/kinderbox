#!/usr/bin/env python
import os, sys, getopt
import time, shutil
import albuminfo, albumcover, albumid, albumplaylist
from os.path import expanduser
sys.path.append("/home/pi/db/")
import DBModule

db = DBModule.DBUtils()

def hasMediaFiles(path):
    for filename in sorted(os.listdir(path)):
        if filename.endswith('.mp3'):
            return True
    return False

def rollback(path, barcodeid):
    #Remove database and m3u:
    if barcodeid is not None:
        db.delete_item_by_barcodeid(barcodeid)
        os.remove("/var/lib/mpd/playlists/%s.m3u" %barcodeid)
    #Remove datafile:
    shutil.rmtree(path)

def main(argv):
    try:
        path = "."
        if len(argv) > 0:
            path = argv[0]
        if not os.path.exists(path) and not os.path.isdir(path):
            raise Exception("expecting path!")

        if not hasMediaFiles(path):
            raise Exception("skipping empty folder (no media files) ... ")

        print "\n\n========================================================================\n"
        print "Album: %s" % path
        print "Create album info"
        albuminfo.create(path)

        print "\n----------------------------------------------------------------------------"
        print "Create album barcode id"
        info = albumid.create(path)

        #print "\n----------------------------------------------------------------------------"
        #print "Create album rfid"
        #cmd = 'python createalbumrfid.py "%s"' % (path)
        #print cmd
        #os.system(cmd)

        print "\n----------------------------------------------------------------------------"
        print "Create album cover"
        print albumcover.create(path)

        print "\n----------------------------------------------------------------------------"
        print "Create playlist m3u "
        print albumplaylist.create(path)

        print "\n----------------------------------------------------------------------------"
        print "Add to database"
        if info is None or len(info) !=2:
            raise Exception("Abum barcodeid and name have error.")
        db.insert_item(None,info[0],info[1])
        print "Finish an album."

    except Exception, ex:
        print "Error Album Info Fail"
        print "Detail: %s" %ex
        if info is None or len(info) !=2:
            rollback(path, None)
        else:
            rollback(path, info[0])
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])

