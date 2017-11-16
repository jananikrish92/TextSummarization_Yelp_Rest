import sqlite3
import DBSetup
from collections import defaultdict

dbmgr = DBSetup.DatabaseManager("nlp.db")

def getPredictedStars():
	predictedStars = defaultdict(float)
	select_stmt = 'select business_id,predicted_score from review;'
	rows = (dbmgr.query(select_stmt)).fetchall()
	n =0
	for row in rows:
		print "business_id:", row[0][0]
		print "predicted_score", row[0][1]
		break
		predictedStars[row[0][0]] += row[0][1]
		n += 1
	for i in predictedStars.keys():
		predictedStars[i] /= n #average
	return predictedStars

def getActualStars():
	actualStars = defaultdict(float)
	select_stmt = 'select business_id,predicted_score from business;'
	rows = (dbmgr.query(select_stmt)).fetchall()
	for row in rows:
		print "business_id:", row[0][0]
		print "predicted_score", row[0][1]
		break
		actualStars[row[0][0]] = row[0][1]
	return actualStars

def evaluation(predictedStars, actualStars):
	rel_error = 0
	for key in predictedStars:
		rel_error += abs(predictedStars[key] - actualStars[key]) / (abs(predictedStars[key]) + abs(actualStars[key]))
	return rel_error

predicted = getPredictedStars()
actual = getActualStars()
rel_error = evaluation(predicted, actual)
print "relative error is" , rel_error