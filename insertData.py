import sqlite3
import json
import DBSetup

dbmgr = DBSetup.DatabaseManager("nlp.db")
file_directory = 'dataset/'
insert_stmt_business = 'INSERT INTO business values(?,?,?,?);'
business_ids = set()
insert_stmt_review = 'INSERT INTO review values(?,?,?,?,?,?);'
insert_stmt_tip = 'INSERT INTO tip values(?,?,?,?);'
insert_stmt_user = 'INSERT INTO user values(?,?,?);'
user_ids = set()
tip_user_id = set()
def business_upload(file_directory):
	data = []
	global business_ids
	with open(file_directory+'business.json') as f:
	    for line in f:
	        data.append(json.loads(line))


	for i in range(len(data)):
		if 'Restaurants' in data[i]['categories']:
			dbmgr.insertQuery1(insert_stmt_business,data[i]['business_id'],data[i]['name'],data[i]['stars'],data[i]['review_count'])
			business_ids.add(data[i]['business_id'])


def review_upload(file_directory):
	data = []
	global user_ids
	global business_id
	with open(file_directory+'review.json') as f:
	    for line in f:
	        data.append(json.loads(line))

	for i in range(len(data)):
		if data[i]['business_id'] in business_ids:
			dbmgr.insertQuery2(insert_stmt_review,data[i]['review_id'],data[i]['user_id'],data[i]['business_id'],data[i]['stars'],data[i]['text'],data[i]['useful'])
			user_ids.add(data[i]['user_id'])


def tip_upload(file_directory):
	data = []
	global user_ids
	global business_ids
	with open(file_directory+'tip.json') as f:
	    for line in f:
	        data.append(json.loads(line))

	for i in range(len(data)):
		if data[i]['business_id'] in business_ids:
			dbmgr.insertQuery1(insert_stmt_tip,data[i]['text'],data[i]['business_id'],data[i]['user_id'],data[i]['likes'])
			user_ids.add(data[i]['user_id'])

def user_upload(file_directory):
	data = []
	global user_ids
	with open(file_directory+'user.json') as f:
	    for line in f:
	        data.append(json.loads(line))

	for i in range(len(data)):
		if data[i]['user_id'] in user_ids:
			dbmgr.insertQuery3(insert_stmt_user,data[i]['user_id'],data[i]['review_count'],data[i]['yelping_since'])
	

business_upload(file_directory)
print "business done"
review_upload(file_directory)
print "review done"
tip_upload(file_directory)
print "tip done"
user_upload(file_directory)
print "user done"
dbmgr.closedDb()
print "the end!!"
