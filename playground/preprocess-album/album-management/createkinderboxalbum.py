#!/usr/bin/env python
import os, sys, getopt
import time
from os.path import expanduser

def hasMediaFiles(path):
	for filename in sorted(os.listdir(path)):
		if filename.endswith('.mp3'):
        		return True
	return False

def main(argv):
	path = "."
	if len(argv) > 0:
      		path = argv[0]
   	if not os.path.exists(path) and not os.path.isdir(path):
      		print "expecting path!"
      		return   
   
   	if not hasMediaFiles(path):
      		print "skipping empty folder (no media files) ... "
      		return   
 

	print "\n\n========================================================================\n"
	print "Album: %s" % path
	print "Create album info"

	cmd = 'python createalbuminfo.py "%s"' % (path)
   	print cmd
   	os.system(cmd)
	
	print "\n----------------------------------------------------------------------------"
	print "Create album barcode id"

   	cmd = 'python createalbumid.py "%s"' % (path)
   	print cmd
	os.system(cmd)
	
	print "\n----------------------------------------------------------------------------"
	print "Create album rfid"
	cmd = 'python createalbumrfid.py "%s"' % (path)
	print cmd
	os.system(cmd)

   	print "Finish an album."
   
if __name__ == "__main__":
    main(sys.argv[1:])

