#!/usr/bin/python

import MySQLdb

#DB connect details

dbname = 'checker'
dbuser = 'checker'
dbpass = 'checker'

class DbHandler():
    ''' Handles all database transport '''
    def __init__(self):
        
        self.db = MySQLdb.connect(db=dbname,user=dbuser,passwd=dbpass,host='localhost',)
        return

    def fetch(self):
        cursor = self.db.cursor()
        query = "SELECT * FROM `submissions` order by time ASC"
        cursor.execute(query)
        res = cursor.fetchone()
        cursor.close()
        return res

    def getUserName(self,uid):
        cursor = self.db.cursor()
        query = " SELECT `handle` FROM `users` WHERE `user_id` = '" + str(uid) + "'"
        a = cursor.execute(query)
        cursor.close()
        user = str(a[0])
        return user

    def getProblemName(self,pid):
        cursor = self.db.cursor()
        query = " SELECT `pcode` FROM `problems` WHERE `pid` = '" + str(pid) + "'"
        a = cursor.execute(query)
        cursor.close()
        prob = str(a[0])
        return prob
    
    def getProblemType(self,pid):
        cursor = self.db.cursor()
        query = " SELECT `ptype` FROM `problems` WHERE `pid` = '" + str(pid) + "'"
        a = cursor.execute(query)
        cursor.close()
        ptype = str(a[0])
        return ptype
    
    def getTimeLimit(self,pid):
        cursor = self.db.cursor()
        query = " SELECT `time_limit` FROM `problems` WHERE `pid` = '" + str(pid) + "'"
        a = cursor.execute(query)
        cursor.close()
        tlimit = int(a[0])
        return tlimit
    
    def getMemLimit(self,pid):
        cursor = self.db.cursor()
        query = " SELECT `mem_limit` FROM `problems` WHERE `pid` = '" + str(pid) + "'"
        a = cursor.execute(query)
        cursor.close()
        mlimit = int(a[0])
        return mlimit
    
    
# debug run here
if __name__ == "__main__":
    a = FetchSubmission();
    ans = a.fetch()
