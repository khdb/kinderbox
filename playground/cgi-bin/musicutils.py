import subprocess
import cgi, os
import StringIO
import LoggerModule

target_folder = "/var/lib/mpd/music"
temp_folder   = "/var/www/cgi-bin/temp"
#archive_file  = "/var/www/cgi-bin/archive.log"
original_folder_name = 'test'

def process(filename):
    try:
        #os.system("echo %s >> upload.log" % filename)
        #test if the archive contains mp3 files
        #os.system("echo '*********************\n' >> %s" % archive_file)
        #os.system("tar -tzf %s/%s >> %s " % (temp_folder, filename, archive_file) )
        #output = os.system("tar -tvf %s/%s " % (temp_folder, filename) )
        #determine if archieve file is tar, zip or gz
        is_mp3 = False
        if filename.endswith('.gz') or filename.endswith('.tar'):
            args = "tar -tzf %s/%s" % (temp_folder, filename)
            print args
            is_mp3 = test_tar(args)
        if filename.endswith('.zip'):
            # or use: zipinfo -1 archive.zip
            args = "unzip -Z -1 '%s/%s'" % (temp_folder, filename)
            print args
            is_mp3 = test_zip(args)

        if is_mp3:
            #unzip the archieve file to /var/lib/mpd/music/
            extract(filename)
            #perform_mpc_update()
            perform_create_info_album()
            #perform_create_playlist()
            #change_ownership(original_folder_name)
            change_ownership() #change ownership of the entire music diretory recursively
            return #return if everything is done.
    except Exception ,ex:
            #at this point there is an error occured!
            logger = LoggerModule.Logger("Music utils")
            logger.error("%s" %ex)
            print "oops, something went wrong."
            print ex
            sys.exit(1)
    finally:
            os.remove(os.path.join(temp_folder,filename))


def test_tar(args):

    #store the programm output to a variable instead of a text file.
    #process the variable line by line and check if contains mp3 files.
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    #print "program output:", out
    buf = StringIO.StringIO(out)
    #print buf.readline()
    a = buf.readline() #the firstline is the target directory in the archieve file
    global original_folder_name #needed to modify global copy of original_folder_name
    original_folder_name = a.rstrip();
    print "original folder_name is: %s " % original_folder_name
    is_mp3 = False
    while a != '':
        a = a.rstrip() #remove new line character
        print a
        is_mp3 = a.endswith('.mp3')
        print is_mp3
        if is_mp3:
            #return True
            break
        a = buf.readline()
    print "file is mp3? %s" % is_mp3
    return is_mp3

def test_zip(args):

    #store the programm output to a variable instead of a text file.
    #process the variable line by line and check if contains mp3 files.
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    #print "program output:", out
    buf = StringIO.StringIO(out)
    #print buf.readline()
    a = buf.readline() #the firstline is the target directory in the archieve file
    global original_folder_name #needed to modify global copy of original_folder_name
    original_folder_name = a.rstrip();
    print "original foldername: is: %s " % original_folder_name
    is_mp3 = False
    while a != '':
        a = a.rstrip() #remove new line character
        print a
        is_mp3 = a.endswith('.mp3')
        print is_mp3
        if is_mp3:
            #return True
            break
        a = buf.readline()
    print "file is mp3? %s" % is_mp3
    return is_mp3
    #return False


def extract(filename):

    if filename.endswith('.gz') or filename.endswith('.tar'):
        print "extract archieve to target directory"
        args = "sudo tar -xzvf %s/%s --directory %s" % (temp_folder, filename, target_folder)
        print args
        #print original_folder_name
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print out
    if filename.endswith('.zip'):
        print "extract archieve to target directory"
        args = "sudo unzip '%s/%s' -d %s" % (temp_folder, filename, target_folder)
        print args
        #print original_folder_name
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print out


def change_ownership():
    #do something here
    print "change ownership of new folder"
    #path = "'%s/%s'" % (target_folder, foldername)
    args = "sudo chown pi:pi -R %s" % target_folder
    print args
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print out
    print err

  
def perform_mpc_update():
    print "Updating mpc database"
    args = "mpc update"
    print args
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print out
    
    
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
    #createkinderboxalbum.py /var/lib/mpd/music/Top 2
    args = "sudo python createkinderboxalbum.py '%s/%s'" % (target_folder, original_folder_name)
    #args = "./start.sh"
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

#print



