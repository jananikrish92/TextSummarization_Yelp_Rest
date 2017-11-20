import sqlite3
import DBSetup
from collections import defaultdict
import pickle

dbmgr = DBSetup.DatabaseManager("nlp.db")

def getPredictedStars():
	predictedStars = defaultdict(float)
	sentimentScores = pickle.load( open( "sentimentScores.p", "rb" ) )
	business_list = pickle.load( open( "reviewToBusiness.p", "rb" ) )
	review_count = defaultdict(float)


	for review in sentimentScores:
		predictedStars[business_list[review]] += sentimentScores[review]
		review_count[business_list[review]] += 1

	for i in predictedStars:
		predictedStars[i] /= review_count[i] #average

	pickle.dump(predictedStars, open( "predictedStars.p", "wb" ))

	return predictedStars
	

def getActualStars():
	actualStars = defaultdict(float)
	select_stmt = 'select business_id, stars from business;'
	rows = (dbmgr.query(select_stmt)).fetchall()
	for row in rows:
		actualStars[row[0]] = row[1]
	pickle.dump(actualStars, open( "actualStars.p", "wb" ))
	return actualStars

def evaluation(predictedStars, actualStars):
	# print len(predictedStars)
	miss = 0
	for key in predictedStars:
		#print abs(predictedStars[key] - actualStars[key]) / (abs(predictedStars[key]) + abs(actualStars[key]))
		if (abs(predictedStars[key] - actualStars[key]) / (abs(predictedStars[key]) + abs(actualStars[key])))>=0.4:
			miss +=1
	return miss/float(len(predictedStars))

predicted = getPredictedStars()
# print predicted
actual = getActualStars()
# print actual
rel_error = evaluation(predicted, actual)
print "relative error is" , rel_error