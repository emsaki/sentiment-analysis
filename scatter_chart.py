#!/usr/bin/python3
from highcharts import Highchart
from pymongo import MongoClient
import pymongo
import json
from sqlalchemy import create_engine
import pymysql

con = MongoClient()
db = con['twitterdb']
col = db['tweets']
data = col.find({}, {"user.followers_count":1,\
	"user.friends_count":1,"user.favourites_count":1,"user.statuses_count":1,"user.listed_count":1, "user.name":1}).limit(10)

#engine = create_engine('mysql+pymysql://root:userdb@localhost/osm_db')
#con = engine.connect()
#tweets = con.execute("SELECT MAX(followers_count), MAX(friends_count), MAX(statuses_count), MAX(favourites_count), MAX(listed_count), name FROM users GROUP BY friends_count")
chart = Highchart()


def get_data():	
	c1 = []
	c2 = []
	c3 = []
	c4 = []
	c5 = []

	cat = []
	for tweet in data:
		c1.append(tweet['user']['followers_count'])
		#c2.append(tweet['user']['friends_count'])
		#c3.append(tweet['user']['statuses_count'])
		#c4.append(tweet['user']['favourites_count'])
		c5.append(tweet['user']['listed_count'])
		cat.append(tweet['user']['name'])
	
	options = {
		'chart':{'type':'scatter'},
		'title':{'text':'Exploratory Visualization'},
		'legend':{'enabled':True},
		'xAxis':{'categories':cat},
		'yAxis':{'title':{'Record Counts'}},
		}

	chart.set_dict_options(options)

	chart.add_data_set(c1, 'scatter', 'Followers Count')
	#chart.add_data_set(c2, 'scatter', 'Friends Count')
	#chart.add_data_set(c3, 'line', 'Statuses Count')
	#chart.add_data_set(c4, 'line', 'Favourites Count')
	chart.add_data_set(c5, 'line', 'Listed Count')
	chart.save_file('templates/scatter_highchart')

if __name__ == '__main__':
	get_data()