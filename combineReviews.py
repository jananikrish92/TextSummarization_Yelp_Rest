import sqlite3
import DBSetup
from collections import defaultdict
import pickle

dbmgr = DBSetup.DatabaseManager("nlp.db")

def joinReviews():
	combinedReviews = defaultdict(str)
	select_stmt = 'select text, business_id from review limit 10;'
	rows = (dbmgr.query(select_stmt)).fetchall()
	for row in rows:
		combinedReviews[row[1]] += row[0]
	pickle.dump(combinedReviews, open( "combinedReviews.p", "wb" ))
	return 

joinReviews()
dbmgr.closedDb()
