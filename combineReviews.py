import sqlite3
import DBSetup
from collections import defaultdict
import pickle

dbmgr = DBSetup.DatabaseManager("nlp.db")

def joinReviews():
	combinedReviews = defaultdict(str)
	select_stmt = 'select text, business_id from review;'
	rows = (dbmgr.query(select_stmt)).fetchall()
	for row in rows:
		combinedReviews[row[1]] += row[0]
	pickle.dump(combinedReviews, open( "combinedReviews.p", "wb" ))
	return 
def joinTips():
	combinedTips = defaultdict(str)
	select_stmt = 'select text, business_id from tip;'
	rows = (dbmgr.query(select_stmt)).fetchall()
	for row in rows:
		combinedTips[row[1]] += row[0]
	pickle.dump(combinedTips, open( "combinedTips.p", "wb" ))
	return 

#joinReviews()
joinTips()
dbmgr.closedDb()
