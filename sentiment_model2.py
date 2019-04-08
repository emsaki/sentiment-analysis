#importing modules and packages
import re
import os
import random
import pickle

import nltk
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus import TwitterCorpusReader
from nltk.tokenize.casual import TweetTokenizer
from nltk.classify import NaiveBayesClassifier
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation
from pprint import pprint
import process_tweets

#creating a classifier class
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
	
	#creating a feature extractor method
	def extract_features(self, words_list):
		words = set(words_list)
		features = {}
		for word in words:
			key = 'contains({})'.format(word)
			value = word in self._master_wordlist
			features[key] = value
		return features

	#creating a classifier method
	def classify(self, tweet):
		tokens = self.tokenizer.tokenize(tweet)
		features = self.extract_features(tokens)
		tweet = process_tweets.pre_process(tweet)
		for feat in features:
			probability = self._classifier.prob_classify(features)
					
			if probability.max() == 'positive':
				return (tweet + ": " + 'positive')

			else:
				return (tweet + ": " + 'negative')	
		
	def classify_percentages(self, tweet):
		tokens = self.tokenizer.tokenize(tweet)
		features = self.extract_features(tokens)
		tweet = process_tweets.pre_process(tweet)
		pos_count = 0
		neg_count = 0
		total_count = 0
		for feat in features:
			probability = self._classifier.prob_classify(features)
					
			if probability.max() == 'positive':
				pos_count += 1
				
			else:
				neg_count += 1

			total_count = pos_count + neg_count	
		pos_percent = round(100 * (pos_count / total_count), 2) + "%"
		neg_percent = round(100 * (neg_count / total_count), 2)	+ "%"

		return pos_percent, neg_percent	
							


#Creating custom tokenizer to preprocess the tweets to remove urls, mentions and hashtags
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
		self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])

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
			text = self.handle_urls(text)

		if self.transform_handles:
			text = self.fix_handles(text)	
		words = super().tokenize(text)

		if self.stopwords:
			words = self.stop(words)

		if self.stem_words:
			words = self.stem(words)
		return words		

#creating a classifier model function				
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
	frequency_dist.pprint(200)

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

#a function that extracts features from the word list
def	feature_extraction(master_list_of_words):
	def extraction_function(word_list):
		words = set(word_list)
		result = {}
		for word in words:
			result_key = 'contains({})'.format(word)
			result_value = word in master_list_of_words
			result[result_key] = result_value

		return result

	return extraction_function

#the main method
def main():
	classifier, master_wordlist = ClassifierModel()
	print(classifier.show_most_informative_features())

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

