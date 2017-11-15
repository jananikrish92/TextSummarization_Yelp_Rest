import sqlite3

class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def query(self, arg):
        self.cur.execute(arg)
        return self.cur

    def insertQuery1(self,arg, arg1,arg2,arg3,arg4):
        self.cur.execute(arg,(arg1,arg2,arg3,arg4))
        return self.cur

    def insertQuery2(self,arg, arg1,arg2,arg3,arg4,arg5,arg6):
        self.cur.execute(arg,(arg1,arg2,arg3,arg4,arg5,arg6))
        return self.cur
        
    def insertQuery3(self,arg, arg1,arg2,arg3):
        self.cur.execute(arg,(arg1,arg2,arg3))
        return self.cur
    
    def closedDb(self):
        self.conn.commit()
        self.conn.close()
