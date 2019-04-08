from highcharts import Highchart
import pandas as pd
import re
from pymongo import MongoClient

chart = Highchart()

def search_word(word, text):
	word = word.lower()
	text = text.lower()
	match = re.search(word, text)
	if match:
		return True	

def create_graph():	
	con = MongoClient()
	db = con['twitterdb']
	tweets = db['tweets'].find()
	#tweets = get_tweets()
	#tweetsnp = bsonnumpy.sequence_to_ndarray(tweets['text'])
	df = pd.DataFrame(list(tweets))
	#sentiwords = ['Joy','Sadness', 'Anger', 'Fear', 'Disgust', 'Suprise']
	df['joy'] = df['text'].apply(lambda text: search_word('joy', text))
	df['sad'] = df['text'].apply(lambda text: search_word('sad', text))
	df['anger'] = df['text'].apply(lambda text: search_word('anger', text))
	df['fear'] = df['text'].apply(lambda text: search_word('fear', text))
	df['disgust'] = df['text'].apply(lambda text: search_word('disgust', text))
	df['happy'] = df['text'].apply(lambda text: search_word('happy', text))	
	#creating word counts
	c1 = df['joy'].value_counts().tolist()
	c2 = df['sad'].value_counts().tolist()
	c3 = df['anger'].value_counts().tolist()
	c4 = df['fear'].value_counts().tolist()
	c5 = df['disgust'].value_counts().tolist()
	c6 = df['happy'].value_counts().tolist()	
	cat = 'Words'
	#chart options
	options = {
		'chart':{'type':'bar'},
		'title':{'text':'Emotional Words in Tweets'},
		'legend':{'enabled':True},
		'xAxis':{'categories':cat},
		'yAxis':{'title':{'Word Frequencies'}},
		}
	#plotting data on a chart
	chart.set_dict_options(options)
	chart.add_data_set(c1, 'bar', 'Joy')
	chart.add_data_set(c2, 'bar', 'Sadness')
	chart.add_data_set(c3, 'bar', 'Anger')
	chart.add_data_set(c4, 'bar', 'Fear')
	chart.add_data_set(c5, 'bar', 'Disgust')
	chart.add_data_set(c6, 'bar', 'Happy')
	chart.save_file('templates/words_highchart')
if __name__ == '__main__':
	create_graph()



	