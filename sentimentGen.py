import sqlite3
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import DBSetup
import time
from collections import defaultdict
import pickle

dbmgr = DBSetup.DatabaseManager("nlp.db")
sid = SentimentIntensityAnalyzer()
def alter_table(table_name):
	stm = 'alter table '+table_name+' add column predicted_score real;'
	dbmgr.query(stm)

def score_eval(score):
	if score >=-1 and score < -0.6:
		return 1
	elif score >=-0.6 and score < -0.2:
		return 2
	elif score >=-0.2 and score < 0.2:
		return 3
	elif score >=0.2 and score < 0.6:
		return 4
	else:
		return 5



def sentiment_review():
	global sid
	global dbmgr
	t0 = time.time() 
	select_stmt = 'select review_id,text from review limit 100;'
	rows = (dbmgr.query(select_stmt)).fetchall()
	dbmgr.closedDb()
	dbmgr = DBSetup.DatabaseManager("nlp.db")

	count = 1
	for row in rows:
		score = score_eval(sid.polarity_scores(row[1])['compound'])
		update_std = 'update review set predicted_score ='+str(score)+' where review_id=\''+str(row[0])+'\';'
		dbmgr.query(update_std)
		print count
		count +=1
	t1 = time.time()
	print "time taken:", t1-t0

def sentiment_review_updated():
	global sid
	global dbmgr
	select_stmt = 'select review_id,text, business_id from review;'
	rows = (dbmgr.query(select_stmt)).fetchall()
	dbmgr.closedDb()
	dbmgr = DBSetup.DatabaseManager("nlp.db")
	business_list = defaultdict(float)
	score_list = defaultdict(float)
	count = 1
	for row in rows:	
		business_list[row[0]] = row[2]
		score = score_eval(sid.polarity_scores(row[1])['compound'])
		score_list[row[0]] = score
		print count
		count +=1
	pickle.dump(score_list, open( "sentimentScores.p", "wb" ))
	pickle.dump(business_list, open('reviewToBusiness.p', "wb"))

def sentiment_tip():
	global sid
	global dbmgr
	select_stmt = 'select id,text from tip;'
	rows = (dbmgr.query(select_stmt)).fetchall()
	dbmgr.closedDb()
	dbmgr = DBSetup.DatabaseManager("nlp.db")
	for row in rows:
		score = score_eval(sid.polarity_scores(row[1])['compound'])
		update_std = 'update tip set predicted_score ='+str(score)+' where id='+str(row[0])+';'
		dbmgr.query(update_std)

#alter_table('review')
sentiment_review_updated()
# alter_table('tip')
# sentiment_tip()
dbmgr.closedDb()