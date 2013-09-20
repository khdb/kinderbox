# -*- coding: cp1252 -*-
import sqlite3 as lite
import sys
from datetime import datetime
import calendar



class DBUtils:


    def __init__(self):
        self.path = "/home/pi/db/kinderbox.db"
        #self.path = "kinderbox.db"

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

            now = datetime.now()
            timestamp = calendar.timegm(now.utctimetuple())
            cur.execute("INSERT INTO item (rfid,barcodeid,name, created_date) VALUES(?,?,?,?)", (rfid, barcodeid, name, timestamp))
            con.commit()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def insert_free_rfid(self, rfid):
        try:
            con = None
            if self.check_rfid_existed(rfid) == False:
                con = lite.connect(self.path)
                cur = con.cursor()
                cur.execute("INSERT INTO free_rfid VALUES(?)", (rfid, ))
                con.commit()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def delete_item_by_barcodeid(self, barcodeid):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("DELETE FROM item WHERE barcodeid=?", (barcodeid,))
            con.commit()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()


    def check_rfid_existed(self, rfid):
        try:
            con = None
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("SELECT * FROM item WHERE rfid=?", (rfid, ))
            rows = cur.fetchall()
            if len(rows) > 0:
                print "1"
                con.close()
                print "2"
                return True
            else:
                cur.execute("SELECT * FROM free_rfid WHERE rfid=?", (rfid, ))
                rows = cur.fetchall()
                print rows
                if len(rows) > 0:
                    print "3"
                    con.close()
                    print "4"
                    return True
                else:
                    con.close()
                    return False
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
            cur.execute("SELECT * FROM item WHERE barcodeid=?", (barcodeid, ))
            rows = cur.fetchall()
            if len(rows) > 0:
                con.close()
                return True
            else:
                con.close()
                return False
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
            cur.execute("UPDATE item SET rfid=?, name=? WHERE barcodeid=?;", (rfid, name, barcodeid, ))
            cur.execute("DELETE FROM free_rfid WHERE rfid=?;", (rfid, ))
            con.commit()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

    def get_all_item(self):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("SELECT rfid, barcodeid, name, DATETIME(created_date, 'unixepoch') FROM item ORDER BY created_date DESC")
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

    def get_all_rfid(self):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            result = []
            #Get bysy rfid
            cur.execute("SELECT rfid FROM item WHERE rfid != null")
            rows = cur.fetchall()
            if (len(rows) > 0):
                for (rfid,) in rows:
                    d = dict(rfid=rfid,free='no')
                    result.append(d)
            #Get free rfid
            cur.execute ("SELECT rfid FROM free_rfid")
            rows = cur.fetchall()
            if (len(rows) > 0):
                for (rfid,) in rows:
                    d = dict(rfid=rfid,free='yes')
                    result.append(d)
            return result
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
            cur.execute("SELECT rfid, barcodeid, name, DATETIME(created_date, 'unixepoch') FROM item WHERE rfid=?", (rfid, ))
            rows = cur.fetchall()
            con.close()
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

    def get_item_by_barcodeid (self, barcodeid):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("SELECT rfid, barcodeid, name, DATETIME(created_date, 'unixepoch') FROM item WHERE barcodeid=?", (barcodeid, ))
            rows = cur.fetchall()
            con.close()
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


    def get_free_rfid (self):
        try:
            con = lite.connect(self.path)
            cur = con.cursor()
            cur.execute("SELECT * FROM free_rfid")
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
            cur.execute("SELECT rfid, barcodeid, name, DATETIME(created_date, 'unixepoch') FROM item WHERE rfid is null ORDER BY created_date DESC")
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


