from data import get_tweets
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
	df['suprise'] = df['text'].apply(lambda text: search_word('suprise', text))
	df['shame'] = df['text'].apply(lambda text: search_word('shame', text))
	df['guilt'] = df['text'].apply(lambda text: search_word('guilt', text))
	df['happy'] = df['text'].apply(lambda text: search_word('happy', text))
	df['embarassment'] = df['text'].apply(lambda text: search_word('embarassment', text))
	df['confuse'] = df['text'].apply(lambda text: search_word('confuse', text))

	c1 = df['joy'].value_counts().tolist()
	c2 = df['sad'].value_counts().tolist()
	c3 = df['anger'].value_counts().tolist()
	c4 = df['fear'].value_counts().tolist()
	c5 = df['disgust'].value_counts().tolist()
	c6 = df['suprise'].value_counts().tolist()
	c7 = df['shame'].value_counts().tolist()
	c8 = df['guilt'].value_counts().tolist()
	c9 = df['happy'].value_counts().tolist()
	c10 = df['embarassment'].value_counts().tolist()
	c11 = df['confuse'].value_counts().tolist()
	
	#Radialize the colors
	chart.setOptions({
    	colors: chart.map(chart.getOptions().colors, function (color):
        	return 
            	radialGradient: {
                	cx: 0.5,
                	cy: 0.3,
                	r: 0.7
            	},
           		stops: [
                	[0, color],
                	[1, chart.Color(color).brighten(-0.3).get('rgb')]  #darken
            	]
        
    	)
	});

	#Build the chart
	chart.chart('container', {
    	chart: {
        	plotBackgroundColor: null,
        	plotBorderWidth: null,
        	plotShadow: false,
        	type: 'pie'
    	},
    	title: {
        	text: 'Word Occurences on Tweets'
    	},
    	tooltip: {
        	pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
   		},
    	plotOptions: {
        	pie: {
            	allowPointSelect: true,
            	cursor: 'pointer',
            	dataLabels: {
                	enabled: true,
                	format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                	style: {
                    	color: (chart.theme && chart.theme.contrastTextColor) || 'black'
                	},
                	connectorColor: 'silver'
            	}
        	}
    	},
    	series: [{
        	name: 'Words',
        	data: [
            	{ name: 'Joy', y: c1 },
            	{
               		name: 'Sadness',
                	y: c2,
                	sliced: true,
                	selected: true
            	},
            	{ name: 'Anger', y: c3 },
            	{ name: 'Fear', y: c4 },
            	{ name: 'Disgust', y: c5 },
            	{ name: 'Suprise', y: c6 },
            	{ name: 'Shame', y: c7 },
            	{ name: 'Guilt', y: c8 },
            	{ name: 'Happy', y: c9 },
            	{ name: 'Embarassment', y: c10 },
            	{ name: 'Confuse', y: c11 }
            

        	]
    	}]
	});

	chart.save_file('templates/pie_highchart')

if __name__ == '__main__':
	create_graph()
