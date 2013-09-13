#!/usr/bin/env python
import os, sys, getopt
import time, glob
from os.path import expanduser

sys.path.append("/home/pi/db")
import DBModule


music_dir = "/var/lib/mpd/music/"
playlist_dir = "/var/lib/mpd/playlists"
temp_dir = "/home/pi/temp"
db = DBModule.DBUtils()


def hasMediaFiles(path):
   for filename in sorted(os.listdir(path)):
      if filename.endswith('.mp3'):
         return True
   return False



def save_playlist(playlist, barcodeid):
   if len(playlist) > 0 and len(barcodeid) > 0:
      print "saving playlist with %d entries" % len(playlist)
      fname = os.path.join(playlist_dir, "%s.m3u" % barcodeid)
      output = open(fname,'w')
      for item in playlist:
         output.write(item)
         output.write("\n")
      output.close()



def main(argv):
    path = "."
    if len(argv) > 0:
        path = argv[0]

    if not os.path.exists(path) and not os.path.isdir(path):
        print "expecting path"
        return

    idfile = os.path.join(path, 'barcode.id')
    if not os.path.exists(idfile):
        print "Missing Barcode.id file"
        return

    current_id = str(open(idfile).read()).strip()
    current_playlist = []
    m3ufile = os.path.join(playlist_dir, '%s.m3u' % current_id)
    if os.path.exists(m3ufile):
        print "Playlist existed"
        return
    os.system("mpc update")

    for f in glob.glob("%s/*.mp3" %path):
        dirName = os.path.basename(os.path.dirname(f))
        fileName = os.path.basename(f)
        current_playlist.append("%s/%s" %(dirName, fileName))

    save_playlist(current_playlist, current_id)

if __name__ == "__main__":
    main(sys.argv[1:])
