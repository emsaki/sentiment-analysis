#importing modules and packages
from flask import Flask, render_template, flash, request, redirect, make_response, send_file
from data import get_tweets
from pymongo import MongoClient
import pymongo
from io import BytesIO
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#creating a connection to MongoDB server having twitter database and tweets collection
con = MongoClient()
db = con['twitterdb']
col = db['tweets']

#creating a Flask application instance
app = Flask(__name__)
app.secret_key = 'sentiment analysis'

#creating an application route for access on a browser
@app.route('/')
#a function that renders an index page on a browser
def index():
	
	return render_template('index.html')

@app.route('/polarity_percent')
def polarity_percent():
	return render_template('pie_highchart.html')

#creating an application route for access on a browser
@app.route('/sentiment')
#a function that renders the sentiment classification results on a browser 
def sentiment():

	tweets, pagination, page, per_page = get_tweets()
	return render_template('polarity.html',
					heading = 'Sentiment Analysis',
					tweets = tweets,
					pagination=pagination,
					page=page,
					per_page=per_page
					)


@app.route('/bargraph')
def bargraph():

	return render_template('bar_highchart.html')


@app.route('/linegraph')
def linegraph():
	
	return render_template('line_highchart.html')

@app.route('/sentigraph')
def sentigraph():
	
	return render_template('words_highchart.html')


@app.route('/tweets_map')
def map():
	# Map size
	fig = plt.figure(figsize=(18,6), dpi=200)
	# Set a title
	plt.title("Tweets Around the World")

	# Declare map projection, size and resolution
	map = Basemap(projection='merc',
	              llcrnrlat=-80,
	              urcrnrlat=80,
	              llcrnrlon=-180,
	              urcrnrlon=180,
	              lat_ts=20,
	              resolution=None, width=8E6, height=8E6)

	#create bluemarble image
	map.bluemarble(scale=0.3)
	#retrieving tweets from a database
	tweets = col.find()
	#getting latitudes and longitudes
	for tweet in tweets:
		if tweet["coordinates"] != None:
			lat = tweet["coordinates"]["coordinates"][0]
			lon = tweet["coordinates"]["coordinates"][1]
			x, y = map(lat, lon)
			map.plot(x, y, 'ro', markersize=2)
	plt.draw()
	figfile = BytesIO()
	fig.savefig(figfile)
	figfile.seek(0)
	return send_file(figfile, mimetype='image/png')
	


if __name__ == "__main__":
	app.run(port=8085, debug=True)	