#import modules and packages
from pymongo import MongoClient
import pymongo
from sentiment_model import SentimentClassifier
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter, get_page_args
from flask import request

#creating connection to MongoDB server twitterdb database having tweets collection
con = MongoClient()
db = con['twitterdb']
col = db['tweets']


#creating a function to
def get_tweets():
	page = request.args.get(get_page_parameter(), type=int, default=1)
	per_page = request.args.get(get_per_page_parameter(), type=int, default=20)
	start = page * per_page
	end = (page + 1) * per_page
	#Retrieving data from database, sorting and paginating
	tweets_data = col.find().sort('_id', pymongo.ASCENDING).skip(per_page).limit(end)
	tweets = tweets_data[start:end]
	
	#classifier instance
	sc = SentimentClassifier()
	tweet_data = []
		
	for tweet in tweets:
		#getting a text from a tweet
		text_data = tweet["text"]
		#Convert to a string
		text_data = str(text_data)
		#perform classification
		text_data = sc.classify(text_data)
		#total += 1
		tweet_data.append(text_data)
	#creating Pagination instance
	paginate = Pagination(page=page,per_page=per_page, per_page_parameter='per_page', show_single_page=True, total=tweets.count(), css_framework='foundation',record_name='tweets')		
	return tweet_data, paginate, page, per_page



def class_percent():
	sc = SentimentClassifier()
	tweets = col.find()	
	for tweet in tweets:
		#getting a text from a tweet
		text_data = tweet["text"]
		#Convert to a string
		text_data = str(text_data)
		#perform classification
		pos_sentiment, neg_sentiment = sc.classify_percentages(text_data)

	return pos_sentiment, neg_sentiment	
		