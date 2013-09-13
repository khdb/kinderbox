#!/usr/bin/env python
import os, sys, getopt
import time
from os.path import expanduser
import config
import DBModule


music_dir = config.music_dir 
playlist_dir = config.playlist_dir
rfid_map_file = config.rfid_map_file
temp_dir = config.temp_dir
db = DBModule.DBUtils()


def hasMediaFiles(path):
   for filename in sorted(os.listdir(path)):
      if filename.endswith('.mp3'):
         return True
   return False


def new_id():
    time.sleep(0.02)
    ret = str(time.time()).replace('.','')
    if len(ret) < 12:
      ret = ret + '0'
    return ret


def getFolderListRecursive(path):
   flist = []
   flist.append(path)
   retlist = []
   while len(flist) > 0:
      current_f = flist.pop(0)
      for element in os.listdir(current_f):
         if os.path.isdir(element):
            new_path = os.path.join(current_f, element)
            flist.append()

def save_playlist(playlist, barcodeid):
   if len(playlist) > 0 and len(barcodeid) > 0:
      print "saving playlist with %d entries" % len(playlist)
      fname = os.path.join(playlist_dir, "%s.m3u" % barcodeid)
      output = open(fname,'w')
      for item in playlist:
         output.write(item)
         output.write("\n")
      output.close()

def getRFIDs(rfidfile):
    rfidlist = []
    if os.path.exists(rfidfile) and os.path.isfile(rfidfile):
        for line in open(rfidfile):
            rfid = line.strip()
            if rfid and len(rfid) > 0:
                rfidlist.append(rfid)
    return rfidlist



def main(argv):
    allsongs_file = os.path.join(temp_dir, 'all.txt')
    cmd = 'mpc listall > "%s"' % allsongs_file
    print cmd
    os.system(cmd)

    current_playlist = []
    current_id = ""
    last_dirname = ""
    rfidfile = ""
    f = open(allsongs_file)
    for line in f:
        line = line.strip()
        dname = os.path.dirname(line)
        if not dname == last_dirname:
            save_playlist(current_playlist, current_id)
            current_playlist = []

            print "preparing new playlist: %s" % dname
            path = os.path.join(music_dir, dname)
            idfile = os.path.join(path, 'barcode.id')
            rfidfile = os.path.join(path, 'rfid.id')
            if not os.path.exists(idfile):
                print "ERROR: missing bardcode.id file in %s" % path
                continue
            else:
                current_id = str(open(idfile).read()).strip()
        #else:
            #print os.path.dirname(line)
        current_playlist.append(line)
        last_dirname = dname
    # save last open playlist
    save_playlist(current_playlist, current_id)

if __name__ == "__main__":
    main(sys.argv[1:])
