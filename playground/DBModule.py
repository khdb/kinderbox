# -*- coding: cp1252 -*-
import sqlite3 as lite
import sys

class DBUtils:
    def __init__(self):
        print "Hello DBUtils"
        self.path = "/home/pi/db/kinderbox.db"

    def get_sql_lite_version(self):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()
            print "SQLite version: %s" % data
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def insert_item(self, rfid, barcodeid, name):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("INSERT INTO item VALUES(?,?,?)", (rfid, barcodeid, name))
            con.commit()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def check_rfid_existed(self, rfid):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("SELECT * FROM item WHERE rfid=%s" %(rfid))
            rows = cur.fetchall()
            con.close()
            if len(rows) > 0:
                return True;
            else:
                return False;
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def check_barcodeid_existed(self, barcodeid):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("SELECT * FROM item WHERE barcodeid=%s" %(barcodeid))
            rows = cur.fetchall()
            con.close()
            if len(rows) > 0:
                return True;
            else:
                return False;
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def update_item_by_rfid(self, rfid, barcodeid, name):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("UPDATE item SET barcodeid=?, name=? WHERE rfid=?", (barcodeid, name, rfid))
            con.commit()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def update_item_by_barcodeid(self, rfid, barcodeid, name):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("UPDATE item SET rfid=?, name=? WHERE barcodeid=?", (rfid, name, barcodeid))
            con.commit()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def get_item_by_rfid (self, rfid):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("SELECT * FROM item WHERE rfid=%s" %(rfid))
            rows = cur.fetchall()
            con.close()
            if (len(rows) > 0):
                return rows
            else:
                return None
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def get_free_rfid (self):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("SELECT * FROM item WHERE barcodeid is null")
            rows = cur.fetchall()
            if (len(rows) > 0):
                return rows[0]
            else:
                return None
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def get_free_album(self):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("SELECT * FROM item WHERE rfid is null")
            rows = cur.fetchall()
            if (len(rows) > 0):
                return rows[0]
            else:
                return None
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()


