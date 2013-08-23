import subprocess
import re

process = subprocess.Popen(['mpc'], shell=True, stdout=subprocess.PIPE)
(st, er) = process.communicate()
track_count = 0
current_track = 0
play_status = 0
try:
    found = re.findall('\[(.*?)\]', st)
    if len(found) > 0:
        if found[0] == 'paused':
            play_status = 1
        else:
            # playing
            play_status = 2
        found = re.findall('#(.*?)/', st)
        if len(found) > 0:
            current_track = int(found[0].strip())
            print "current track = %d" % current_track
        found = re.findall('#.*/(.*?)\s\s', st)
        if len(found) > 0:
            track_count = int(found[0].strip())
            print "track count = %d" % track_count
except ValueError, ex:
    print '"%s" cannot be converted to an int: %s' % (found[0], ex)
