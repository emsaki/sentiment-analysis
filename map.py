import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pymongo import MongoClient
from mpld3 import save_html

con = MongoClient()
db = con['twitterdb']
col = db['tweets']

def draw_map():
	# Map size
	fig = plt.figure(figsize=(18,4), dpi=250)
	# Set a title
	plt.title("Tweets around the World")

	# Declare map projection, size and resolution
	map = Basemap(projection='merc',
	              llcrnrlat=-80,
	              urcrnrlat=80,
	              llcrnrlon=-180,
	              urcrnrlon=180,
	              lat_ts=20,
	              resolution=None)

	#create bluemarble image
	map.bluemarble(scale=0.3)
	tweets = col.find()
	for tweet in tweets:
		if tweet["coordinates"] != None:
			lat = tweet["coordinates"]["coordinates"][0]
			lon = tweet["coordinates"]["coordinates"][1]
			x, y = map(lat, lon)
			map.plot(x, y, 'ro', markersize=2)
	plt.draw()
	fig.savefig('mapimg.jpg')
	#save_html(fig, 'templates/map.html')
	# Set interactive mode OFF
	plt.ion()

	# Display map
	plt.show()

if __name__ == '__main__':
	draw_map()
