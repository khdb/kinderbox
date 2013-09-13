import subprocess
import cgitb, os
import StringIO
import LoggerModule

cgitb.enable()

logger = LoggerModule.Logger()

def process():
    logger.error("Start update kinderbox")
    perform_create_info_album()
    perform_create_playlist()
    logger.error("Finish update kinderbox")


def perform_create_info_album():
    print "Creating new info album"
    #do something
    location = "/home/pi/huy-projects/kinderbox/playground/preprocess-album/album-management/"
    #args = "sudo /home/pi/huy-projects/kinderbox/playground/preprocess-album/album-management/start.sh"
    #cmd = "cd %s" % location
    #print cmd
    #os.system("cd /home/pi/huy-projects/")
    os.chdir(location)
    os.system("pwd")
    args = "./start.sh"
    print args
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print out

def perform_create_playlist():
    print "Creating new playlist"
    #do something
    location = "/home/pi/huy-projects/kinderbox/playground/createplaylist.py"
    args = "sudo python %s" %location
    print args
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print out

print "Content-Type: text/html;charset=UTF-8"
print
process()
