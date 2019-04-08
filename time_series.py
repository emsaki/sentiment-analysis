#!/usr/bin/python3
from highcharts import Highchart
from pymongo import MongoClient
import json
import pymysql

con = MongoClient()
db = con['twitterdb']
col = db['tweets']
data = col.find().limit(10)
chart = Highchart()


def get_data():	
	c = []

	for tweet in data:
		c.append(tweet['created_at'])
		#cat.append(tweet['user']['name'])
	
	options = {
		'chart':{'type':'line'},
		'title':{'text':'Exploratory Visualization'},
		'legend':{'enabled':True},
		'xAxis':{'categories':c},
		'yAxis':{'title':{'Record Counts'}},
		}

	chart.set_dict_options(options)

	chart.add_data_set(c, 'line', 'Tweet Created Date')
	chart.save_file('templates/time-highchart')

if __name__ == '__main__':
	get_data()