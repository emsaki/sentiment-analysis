from pymongo import MongoClient
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from string import punctuation
from wordcloud import WordCloud
from nltk.corpus import stopwords
from string import punctuation


def wordCloud():
	"""a function to get text data from database and return the same"""
	con = MongoClient()
	db = con.twitterdb
	col = db.tweets
	tweets = col.find()
	text_data = []
	for tweet in tweets:
		text = tweet['text']
		text_data.append(text)
	text_data = str(text_data)
	text_data = text_data.lower()

	#create a set of stopwords to be removed from text
	stopWords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL', 'https', 'co'])

	#tokenize the sentences into words
	text_words = word_tokenize(text_data)

	#creates a wordcloud
	wordcloud = WordCloud(stopwords=stopWords,background_color='white').generate(' '.join(text_words))
	wordcloud.to_file("templates/tweets_wordcloud.png")
	word_cloud = plt.figure(figsize=(25,15))
	plt.title("WordCloud")
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()
	return word_cloud

if __name__ == '__main__':
	wordCloud()						
	