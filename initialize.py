import DBSetup

dbmgr = DBSetup.DatabaseManager("nlp.db")

def createTableBusiness():
  dbmgr.query("CREATE TABLE IF NOT EXISTS business(business_id char(100),name char(100),stars real,review_count real)")

def createTableReview():
  dbmgr.query("CREATE TABLE IF NOT EXISTS review(review_id char(100),user_id char(100),business_id char(100),stars real,text text,useful real)")

def createTableTip():
  dbmgr.query("CREATE TABLE IF NOT EXISTS tip(id integer primary key autoincrement, text text,business_id char(100),user_id char(100),likes real)")

def createTableUser():
  dbmgr.query("CREATE TABLE IF NOT EXISTS user(user_id char(100),review_count real,yelping_since date)")



def callCreateDBSchema():
       createTableBusiness()
       createTableReview()
       createTableTip()
       createTableUser()




