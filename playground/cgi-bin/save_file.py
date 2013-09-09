import cgi, os
import cgitb; cgitb.enable()
import musicutils as util

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
        pass

form = cgi.FieldStorage()

# A nested FieldStorage instance holds the file
fileitem = form['uploader2']

# Test if the file was uploaded
if fileitem.filename:
    with open("log.txt",'wb') as myfile:
        myfile.write(fileitem.filename)
    #strip leading path from file name to avoid directory traversal attacks
    fn = os.path.basename(fileitem.filename)
    fout = file ('temp/' + fn, 'wb')
    while 1:
        chunk = fileitem.file.read(1000000)
        if not chunk: break
        fout.write(chunk)
        fout.flush()
        os.fsync(fout)
    fout.close()
    #open('temp/' + fn, 'wb').write(fileitem.file.read())
    message = 'The file "' + fn + '" was uploaded successfully'
    #prepare for unpack and mv to music folder
    util.process(fn);
else:
    message = 'No file was uploaded'

print """\
        Content-Type: text/html\n
        <html><body>
        <p>%s</p></body></html>
        """ % (message,)
