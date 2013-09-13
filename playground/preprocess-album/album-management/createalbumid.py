#!/usr/bin/env python
import os, sys, getopt
import time
from os.path import expanduser
sys.path.append("/home/pi/db/")
import DBModule

db = DBModule.DBUtils()
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
    if not os.path.exists(tmp_folder):
        print "creating tmp folder ..."
        os.makedirs(tmp_folder)
    cmd = "rm -rf %s" % (os.path.join(tmp_folder, '*'))
    os.system(cmd)
    ps_file  = os.path.join(tmp_folder, 'barcode.ps')
    id_file  = os.path.join(path, 'barcode.id')
    png_file = os.path.join(path, 'barcode.png')

    if os.path.exists(id_file):
        id_string = str(open(id_file).read()).strip()
        print "using id %s" % id_string
    else:
        print "creating new id ..."
        while 1:
            id_string = new_id()
            if db.check_barcodeid_existed(id_string) == False:
                break
            time.sleep(0.1)
        output = open(id_file,'w')
        output.write(id_string)
        output.close()
    
    #Write album to item table
    if db.check_barcodeid_existed(id_string) == False:
        name = os.path.basename(path)
        if name == "" or name is None:
            name = os.path.basename(os.path.dirname(path))
        db.insert_item(None, id_string, name)

    print "creating id done."

if __name__ == "__main__":
    main(sys.argv[1:])

