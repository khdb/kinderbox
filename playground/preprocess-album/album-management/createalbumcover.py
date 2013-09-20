#!/usr/bin/env python
import os, sys, getopt
import time
from os.path import expanduser

def create_link(path, filename, default_thumb=False):
    print "ready to create symlink"
    print "%s%s" % (path, filename)
    img_file = "%s%s" % (path, filename)
    id_file  = "%s/barcode.id" % path
    # Open a file
    fo_img = open(img_file, "r")
    fo_id  = open(id_file, "r")
    if fo_id and fo_img:
        print "Name of the file: ", img_file
        #barcode_id =
        barcode_id = fo_id.readline()
        print "Read Line: %s" % (barcode_id)
        new_folder = "/var/www/images/%s" % barcode_id
        #if new_folder doesnt exists, then:
        if not os.path.exists(new_folder):
            cmd = "sudo mkdir %s" % new_folder
            print cmd
            os.system(cmd)
            #os.makedirs(new_folder) #in case need root permission, this will not work
            print "default_thumb: %s" % default_thumb
            if not default_thumb:
                #cmd2 = "sudo ln -s '/var/www/images/no-image.jpg' %s/cover.jpg" % (new_folder)
                cmd2 = "sudo ln -s '%s' %s/cover.jpg" % (img_file, new_folder)
            if default_thumb:
                #cmd2 = "sudo ln -s '%s' %s/cover.jpg" % (img_file, new_folder)
                cmd2 = "sudo ln -s '/var/www/images/no-image.jpg' %s/cover.jpg" % (new_folder)
            print cmd2
            os.system(cmd2)


def hasMediaFiles(path):
    for filename in sorted(os.listdir(path)):
        print filename
        if filename.endswith('.jpg'):
            #do something here
            create_link(path, filename, False)
            return True

    #At this point there is no image file found, so create a default thumb file.
    create_link(path, filename, True)
    #print "here ende: %s" % filename
    return False

def main(argv):
	path = "."
	if len(argv) > 0:
      		path = argv[0]
   	if not os.path.exists(path) and not os.path.isdir(path):
      		print "expecting path!"
      		return   
   
   	if not hasMediaFiles(path):
      		print "skipping empty folder (no jpg file) ... "
      		return   
 

	print "\n\n========================================================================\n"
	print "Album: %s" % path
	#print "Create album cover image..."
   	#print "Finish cover processing of album."
   
if __name__ == "__main__":
    main(sys.argv[1:])

