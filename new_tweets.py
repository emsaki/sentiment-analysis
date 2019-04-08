#!/usr/bin/python3
import pymongo
from pymongo import MongoClient
from twython import TwythonStreamer
import json

ConsumerKey = 'mBN0ouW21pX4BNQ5TxkLin8LN'
ConsumerSecret = 'YeiJgXXdUW9B6ygZT2DrkDK5CqOLBGIB4MPpV1NaPfJ3Oyljrh' 
AccessToken = '1336037083-xMng5TXrgTAYVxfV438vV6xB2oP1TjCXY99QIZL' 
AccessTokenSecret = 'n3B5SNgw0GfM2egSQmF5xvX4IPM1Mb3BuFyfQxuzxQ1Mq'


con = MongoClient()
db = con['twitterdb']
col = db['tweets']

class MyStreamer(TwythonStreamer):
	def on_success(self, data):			
		#data = json.loads(data)
		text = data["text"]
		created_at = data["created_at"]
		print(text)
		records = data
		records['_id'] = records['id_str']
		col.insert(records)
		return created_at, text

	def on_error(self, status):
		print(status)
		pass

language = "en"
streamer = MyStreamer(ConsumerKey, ConsumerSecret, AccessToken, AccessTokenSecret)
streamer.statuses.filter(track=['#anger','#fear','#disgust','#sad','#happy', '#shame', '#confuse',\
 '#guilt', '#suprise', '#embarassment', '#joy'], language=language)			
			
