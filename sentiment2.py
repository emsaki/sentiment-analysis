import re
import os
import random
import pickle
import json
import collections


import nltk
import nltk.metrics
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus import TwitterCorpusReader
from nltk.tokenize.casual import TweetTokenizer
from nltk.classify import NaiveBayesClassifier
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation
from pprint import pprint
from pymongo import MongoClient



class SentimentClassifier:
	def __init__(self):
		self.tokenizer = CustomTokenizer()
		self._classifier = None
		self._master_wordlist = None
		classifier_filepath = get_classifier_filepath()
		wordlist_filepath = get_master_wordlist_filepath()
		if not os.path.isfile(classifier_filepath) or not os.path.isfile(wordlist_filepath):
			main()
		with open(classifier_filepath, 'rb') as f:
			self._classifier = pickle.load(f)
		with open(wordlist_filepath, 'rb') as f:
			self._master_wordlist = pickle.load(f)	
	
	def extract_features(self, words_list):
		words = set(words_list)
		features = {}
		for word in words:
			features['contains({})'.format(word)] = (word in self._master_wordlist)
		return features


	def classifying(self, tweets):
		#tokens = self.tokenizer.tokenize(tweet)
		#features = self.extract_features(tokens)
		#print(self._classifier.show_most_informative_features(25))
		NBResultLabels = [self._classifier.classify(self.extract_features(tweet[0])) for tweet in tweets]

		#prints the labels
		#print(NBResultLabels)
		print("This is the Naive Bayes Classification Results")
		
		#print the counts for positive and negative word features contained in the test data (tweets from database) 
		print('Positive labels count: ' + str((NBResultLabels.count('positive'))))
		print('Negative labels count: ' + str((NBResultLabels.count('negative'))))

		#if NBResultLabels.count('positive') > NBResultLabels.count('negative'):
		print('Naive Bayes Result Positive Sentiment: ' + str(round((100*NBResultLabels.count('positive')/len(NBResultLabels)), 1)) + "%")

		#if NBResultLabels.count('positive') < NBResultLabels.count('negative'):
		print('Nave Bayes Result Negative Sentiment: ' + str(round((100*NBResultLabels.count('negative')/len(NBResultLabels)), 1)) + "%")	
		

class CustomTokenizer(TweetTokenizer):
	"""docstring for CustomTokenizer"TweetTokenizeref __init__(self, arg):
		super(CustomTokenizer,TweetTokenizer.__init__()
		self.arg = arg """
	def __init__(self, preserve_case = False, reduce_length = True, remove_urls = True, transform_handles = True, stem_words = True):
		super().__init__(preserve_case, reduce_length, False)
		self.remove_urls = remove_urls
		self.transform_handles = transform_handles
		self.twitter_handles_re = re.compile(r"(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){20}(?!@))|(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){1,19})(?![A-Za-z0-9_]*@)")
		self.urls_re = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\.,<>?\xab\xbb\u201c\u201d\u2018\u2019]))")
		self.stem_words = stem_words
		self._stemmer = SnowballStemmer('english')
		self.stopwords = stopwords
		self._stopwords = set(stopwords.words('english') + list(punctuation))

	def fix_handles(self, text):
		return self.twitter_handles_re.sub('_handle', text)

	def handle_urls(self, text):
		return self.urls_re.sub('_urls', text)

	def stem(self, words):
		return [self._stemmer.stem(word) for word in words]

	def stop(self, words):
		return [word for word in words if not word in self._stopwords]	

	def tokenize(self, text):
	#Text preprocessing
		if self.remove_urls:
			text = str(text)
			text = self.handle_urls(text)

		if self.transform_handles:
			text = self.fix_handles(text)	
		words = super().tokenize(text)

		if self.stopwords:
			words = self.stop(words)

		if self.stem_words:
			words = self.stem(words)
		return words

def ClassifierModel():
	positive_file = 'positive_tweets.json'
	negative_file = 'negative_tweets.json'
	files = [positive_file, negative_file]
	twitter_samples = LazyCorpusLoader('twitter_samples',
										TwitterCorpusReader,
										files,
										word_tokenizer = CustomTokenizer())

	#this returns a list of lists
	twitter_tokens = twitter_samples.tokenized()
	
	#need to unpack the list of lists using nested list
	frequency_dist = nltk.FreqDist(x for sub in twitter_tokens for x in sub)
	#frequency_dist.pprint(200)

	master_list_of_words = tuple(frequency_dist.keys())
	extraction_function = feature_extraction(master_list_of_words)
	positive_tokens = twitter_samples.tokenized(positive_file)
	negative_tokens = twitter_samples.tokenized(negative_file)
	positive_tokens = [(token, 'positive') for token in positive_tokens]
	negative_tokens = [(token, 'negative') for token in negative_tokens]
	all_tokens = positive_tokens + negative_tokens
	random.shuffle(all_tokens)
	
	#creating training set
	training_set = nltk.classify.apply_features(extraction_function, all_tokens)
	
	#creating a classifier bt calling the train method
	classifier = NaiveBayesClassifier.train(training_set)

	return classifier, master_list_of_words

def createTestData():
	connection = MongoClient()
	db = connection['twitterdb']
	col = db['tweets']
	data = col.find()
	tweets = []
	for tweet in data:
		#Convert to lower case
		tweet = tweet['text'].lower()
		tokenizer = CustomTokenizer()
		tweet = tokenizer.tokenize(tweet)
		print(tweet)
		tweets.append(tweet)
	return tweets

def	feature_extraction(master_list_of_words):
	def extract_features(word_list):
		tweet_word = set(word_list)
		features = {}
		for word in tweet_word:
			features['contains({})'.format(word)] = (word in master_list_of_words)
		return features		
	return extract_features
	return extraction_function

def main():
	classifier, master_wordlist = ClassifierModel()
	sentiment = SentimentClassifier()
	testData = createTestData()
	#pprint(testData)
	print(classifier.show_most_informative_features(15))
	sentiment.classifying(testData)
	#print(nltk.metrics.scores.accuracy(master_wordlist, testData))
	#print(accuracy(classifier, testData))
	classifier_filepath = get_classifier_filepath()
	if os.path.isfile(classifier_filepath):
		os.remove(classifier_filepath)

	wordlist_filepath = get_master_wordlist_filepath()
	if os.path.isfile(wordlist_filepath):
		os.remove(wordlist_filepath)

	with open(classifier_filepath, 'wb') as f:
		pickle.dump(classifier, f)

	with open(wordlist_filepath, 'wb') as f:
		pickle.dump(master_wordlist, f)

def get_classifier_filepath():
	directory = os.path.abspath(os.path.dirname(__file__))
	classifier_filepath = os.path.join(directory, 'data', 'naive_bayes_model.pickle')
	return classifier_filepath

def get_master_wordlist_filepath():
	directory = os.path.abspath(os.path.dirname(__file__))
	master_wordlist_filepath = os.path.join(directory, 'data', 'master_wordlist.pickle')
	return master_wordlist_filepath	


if __name__ == '__main__':
	main()

