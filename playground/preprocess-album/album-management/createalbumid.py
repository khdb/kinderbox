#!/usr/bin/env python
import os, sys, getopt
import time
from os.path import expanduser

tmp_folder_name = '.tmp/barcode'

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
   
   	home = expanduser("~")
   	tmp_folder = os.path.join(home, tmp_folder_name)
   	print "checking tmp folder ..."
   	print tmp_folder
   	if not os.path.exists(tmp_folder):
      		print "creating tmp folder ..."
      		os.makedirs(tmp_folder)
   	print "clearing tmp folder ..."
   	cmd = "rm -rf %s" % (os.path.join(tmp_folder, '*'))
   	os.system(cmd)
   	ps_file  = os.path.join(tmp_folder, 'barcode.ps') 
   	id_file  = os.path.join(path, 'barcode.id')
   	png_file = os.path.join(path, 'barcode.png')
   
  	print ps_file
   	print id_file
   	print png_file


   	if os.path.exists(id_file):
      		id_string = str(open(id_file).read()).strip()
      		print "using id %s" % id_string
   	else:
      		print "creating new id ..."
      		id_string = new_id()
      		output = open(id_file,'w')
      		output.write(id_string)
      		output.close()
   
   	if not os.path.exists(png_file):
      		cmd = 'barcode -b "%s" -e ean13 -o "%s"' % (id_string, ps_file)
      		print "executing '%s' ..." % cmd     
      		os.system(cmd)
      		#cmd = 'convert -density 300 -crop 520x400+0+2900 "%s" "%s"' % (ps_file, png_file)
      		#print "executing '%s' ..." % cmd
      		#os.system(cmd)
   	else:
      		print "skipping (barcode.png exists) ..."

   	print "done."
   
if __name__ == "__main__":
    	main(sys.argv[1:])

