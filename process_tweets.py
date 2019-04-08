#import regular expression (regex)
import re
from nltk.corpus import stopwords
from string import punctuation

#pre-process the tweets
def pre_process(tweet):
    # process the tweets
    #tweet = str(tweet)
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    #Convert @username to AT_USER
    #tweet = re.sub('@[^\s]+','',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trimming
    tweet = tweet.strip('\'"')
    return tweet

if '__name__' == '__main__':
    replaceTwoOrMoreCharacter(tweets)
    pre_process(tweets)    