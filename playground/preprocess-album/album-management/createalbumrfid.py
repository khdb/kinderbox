import sys, os
sys.path.append("/home/pi/db")
import DBModule

db = DBModule.DBUtils()


def save_rfid_file(rfid_path, rfid):
    with open(rfid_path, "w") as myfile:
        entry = "%s" % (rfid)
        myfile.write(entry)

def main(argv):
    path = "."
    if len(argv) > 0:
        path = argv[0]

    if not os.path.exists(path) and not os.path.isdir(path):
        print "expecting path!"
        return

    name = os.path.basename(path)
    idfile = os.path.join(path, 'barcode.id')
    rfid_file = os.path.join(path, 'rfid.id')
    if not os.path.exists(idfile):
        print "Missing Barcode.id file"
        return

    barcode_id = str(open(idfile).read()).strip()
    item = db.get_item_by_barcodeid(barcode_id)
    if item is None:
        rfid = None 
    else:
        rfid = item[0]

    if rfid is None:
        #Get new RFID from RFID Management

        rfid = db.get_free_rfid()
        if rfid is None:
            print "Error: Not enough free RFID. Please import new RIFD..."
            return
        else:
            save_rfid_file(rfid_file, rfid)
    else:
        #Update RFID
        save_rfid_file(rfid_file, rfid)

    #Update BarcodeID into RFID Management
    db.update_item_by_barcodeid(rfid, barcode_id, name)


if __name__ == "__main__":
    main(sys.argv[1:])

