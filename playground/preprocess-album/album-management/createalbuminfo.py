#!/usr/bin/env python
#!/usr/bin/env python
import os, eyed3, sys, getopt
import simplejson as json

def secondsToHMS(seconds):
   hours = seconds / 3600
   seconds -= 3600*hours
   minutes = seconds / 60
   seconds -= 60*minutes
   if hours == 0:
      return "%02d:%02d" % (minutes, seconds)
   return "%02d:%02d:%02d" % (hours, minutes, seconds)
    
def getDataString(data):
   if not data:
      return "unknown"
   data = data.strip()
   if len(data) == 0:
      return "unknown"
   return data

def hasMediaFiles(path):
   for filename in sorted(os.listdir(path)):
      if filename.endswith('.mp3'):
         return True
   return False

def getMp3Info(fname):
   print "Test fname = %s" % (fname)
   audiofile = eyed3.load(fname)

   track_str = ""
   (track_num, track_total) = audiofile.tag.track_num
   if track_num is not None:
       track_str = str(track_num)
       if track_total:
          track_str += "/%d" % track_total


   mp3info = {}
   mp3info["album"] = getDataString(audiofile.tag.album)
   #print "mp3info_album = %s" & (mp3info["album"])
   mp3info["artist"] = getDataString(audiofile.tag.artist)
   mp3info["title"] = getDataString(audiofile.tag.title)
   mp3info["genre"] = getDataString(str(audiofile.tag.genre.name))
   mp3info["year"] = getDataString(str(audiofile.tag.recording_date))
   mp3info["track"] = track_str
   #mp3info["track"] = getDataString(str(audiofile.tag.track_num)) 
   mp3info["length"] = 10000
   mp3info["lengthstring"] = "10000"
   #mp3info["length"] = audiofile.play_time
   #mp3info["lengthstring"] = audiofile.playTimeString
   return mp3info

def main(argv):
   count = 0
   path = "."
   
   if len(argv) > 0:
      path = argv[0]
   
   if not os.path.exists(path) and not os.path.isdir(path):
      print "expecting path!"
      return   
   
   if not hasMediaFiles(path):
      print "skipping empty folder (no media files) ... "
      return
   
   outputname = os.path.join(path, 'info.json')

   if os.path.exists(outputname):
      print "info.json does already exist"
      return

   allinfo = {}
   mp3infos = []
   counter = 0
   playtime = 0
   if len(path) > 0:
      for filename in sorted(os.listdir(path)):
         if filename.endswith('.mp3'):
            counter = counter + 1
            fullname = os.path.join(path, filename)            
            mInfo = getMp3Info(fullname)
	    print mInfo
            # take common data from first mp3 file
            if counter == 1:
               	#print "mInfo album = %" % (mInfo["album"])
	 	allinfo["album"] = mInfo["album"]
               	allinfo["artist"] = mInfo["artist"]
               	allinfo["year"] = mInfo["year"]
               	allinfo["genre"] = mInfo["genre"]
            playtime = playtime + mInfo["length"]
            mp3infos.append(mInfo)
   else:
      print "PATH?"
   allinfo["tracks"] = mp3infos
   allinfo["length"] = playtime
   allinfo["lengthstring"] = secondsToHMS(playtime)
   #print allinfo
   jsonstring = json.dumps(allinfo, sort_keys=True, indent=4 * ' ')
   print "writing info.json ..."
   outputfile = open(outputname,'w')
   outputfile.write(jsonstring)
   outputfile.close()
   print "done."

if __name__ == "__main__":
    main(sys.argv[1:])
