#coding: utf-8

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/MySQL_python-1.2.3-py2.7-macosx-10.6-intel.egg')
import time
import MySQLdb
from config import DATABASE as DB

SCORE = [1, 7, 30]
class WTD(object):
    def __init__(self):
        self.items = []

    @property
    def db(self):
        return MySQLdb.connect(
                host=DB['host'], 
                user=DB['user'], 
                passwd=DB['passwd'], 
                db=DB['db'], 
                charset="utf8")

    def sql_execute(self, sql):
        db = self.db
        cursor = db.cursor()
        cursor.execute(sql)
        res =  cursor.fetchall()
        db.commit()
        db.close()
        return res

    def add_item(self, arg, note='NONE'):
        arg = arg.split(' ')
        name, method = arg[0], int(arg[1])
        now = int(time.time())
        sql = """INSERT INTO item (name, method, created, last, note) 
            VALUES( '%s', %d, %d, %d, '%s')"""%(name, method, now, now, note)
        self.sql_execute(sql)

    def update_item(self, iid):
        now = int(time.time())
        sql = "UPDATE item SET last = %d WHERE id = %d"%(now, int(iid))
        self.sql_execute(sql)

    def done_item(self, iid):
        now = int(time.time())
        sql = "UPDATE item SET done = 1 WHERE id = %d"%(int(iid))
        self.sql_execute(sql)

    def getScore(self, method, last):
        return int(time.time()-last) / method

    def show_item(self):
        sql = "SELECT id, name, method, last FROM item WHERE done = 0"
        res = self.sql_execute(sql)
        r = []
        for x in res:
            r.append([x[0], x[1], self.getScore(x[2],x[3]) ])
        r = sorted(r, key=lambda d: -d[2])
        for x in r:
            if x[2] >= 86400:
                print '%s\t%s'%(x[0], x[1].encode('utf-8'))
        return 1

if __name__ == "__main__":
    w = WTD()
    if sys.argv[1] == '-a':
        w.add_item(sys.argv[2])
    elif sys.argv[1] == '-u':
        w.update_item(sys.argv[2])
    elif sys.argv[1] == '-d':
        w.done_item(sys.argv[2])
    elif sys.argv[1] == '-s':
        w.show_item()

        
