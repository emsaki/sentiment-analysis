from pymongo import MongoClient
import pymongo


def get_data():
	"""a function to retieve and data for creating charts using highcharts"""
	#connection to database
	con = MongoClient()
	db = con['twitterdb']
	col = db['tweets']

	#find the data and returns a cursor object
	data = col.find({"user.followers_count":{"$gte":150000}, "user.friends_count":{"$gte":50000}, "user.statuses_count":{"$gte":50000}},\
	{"user.followers_count":1, "user.friends_count":1, "user.statuses_count":1, \
	"user.favourites_count":1, "user.name":1}).limit(10)
	
	c1 = []
	c2 = []
	c3 = []
	c4 = []
	c5 = []
	cat = []

	#iterate through the return cursor object to get the data
	for tweet in data:
		c1.append(tweet['user']['followers_count'])
		c2.append(tweet['user']['friends_count'])
		c3.append(tweet['user']['statuses_count'])
		cat.append(tweet['user']['name'])
	#print(c1,c2,c3,cat)	
	return c1, c2, c3, cat

#run the function
"""
if __name__ == '__main__':
	get_data()
"""	
