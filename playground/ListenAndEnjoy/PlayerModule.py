import sys, os, subprocess, re
import config

class Player:

    def __init__(self):
        print "Init player"
        self.playlist_dir =  config.playlist_dir
        self.track_count = 0
        self.current_track = 1
        self.play_status = 0

    def load_playlist(self, pls):
        pls_file = os.path.join(self.playlist_dir, "%s.m3u" % pls)
        if os.path.exists(pls_file):
            print "loading playlist: %s" % pls
            os.system("mpc stop")
            os.system("mpc clear")
            os.system("mpc load %s" % pls)
            self.track_count = self.get_track_count()
            self.current_track = 1
            if self.track_count > 0:
                os.system("mpc play 1")
        else:
            print "playlist not found!"

    def get_play_status(self):
        process = subprocess.Popen(['mpc'], shell=True, stdout=subprocess.PIPE)
        (st, er) = process.communicate()
        self.track_count = 0
        self.current_track = 0
        self.play_status = 0
        toggle = ""
        message = ""
        try:
            found = re.findall('\[(.*?)\]', st)
            if len(found) > 0:
                if found[0] == 'paused':
                    self.play_status = 1
                    toggle = "PAUSED"
                else:
                    # playing
                    self.play_status = 2
                    toggle = "PLAYING"
            found = re.findall('#(.*?)/', st)
            if len(found) > 0:
                self.current_track = int(found[0].strip())
                #print "current_track = %d" % self.current_track
            found = re.findall('#.*/(.*?)\s\s', st)
            if len(found) > 0:
                self.track_count = int(found[0].strip())
                #print "track count = %d" % self.track_count
            message = "%s \n %s %s" %(toggle, self.current_track, self.track_count)
            return message
        except ValueError, ex:
            print '"%s" cannot be converted to an int: %s' % (found[0], ex)
        return "N/A"

    def get_track_count(self):
        process = subprocess.Popen(['mpc playlist | wc -l'], shell=True, stdout=subprocess.PIPE)
        (st, er) = process.communicate()
        tcount = 0
        try:
            tcount = int(st.strip())
        except ValueError, ex:
            print '"%s" cannot be converted to an int: %s' % (st, ex)
        return tcount


    def process_button(self, button):
        # PREV
        if button == 'PREV':
            if self.current_track > 1:
                self.current_track = self.current_track - 1
                os.system("mpc play %d " % self.current_track)
            else:
                print "Current track is minumum"

        # PLAY/PAUSE
        if button == 'TOGGLE':
            os.system("mpc toggle")

        #NEXT
        if button == 'NEXT':
            if self.current_track < self.track_count:
                self.current_track = self.current_track + 1
                os.system("mpc play %d " % self.current_track)
            else:
                print "Current track is minumum"

        #VOLUME UP
        if button == "VOLUP":
            os.system("mpc volume +5")

        #VOLUME DOWN
        if button == "VOLDOWN":
            os.system("mpc volume -5")


