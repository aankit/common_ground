#this is all about words
import re, nltk
from string import punctuation
from itertools import permutations
from patterns import *
from nltk.tokenize import wordpunct_tokenize
nltk.data.path.append('./tweetEasy/nltk_data/') #this may need to change depending on when
from nltk.corpus import stopwords, words
from collections import Counter
from tweetsql.model import Tweet, Hashtag
from tweetsql.database import db_session

tweets = db_session.query(Tweet.tweet).filter(Tweet.id<500).all()
db_hashtags = db_session.query(Hashtag.hashtag).all()

hashtag_count = Counter()
hashtag_set = set([ht[0].lower() for ht in db_hashtags])
hashtagco = {} #hashtag co-occurence dictionary

word_set = set()
word_count = Counter()
wordco = {} #word co-occcurence dictionary

#helpers
def makeDict(d, k, v):
    if k in d.keys():
        if type(v) is list and len(v)>0:
            for i in v:
                d[k].append(v)
        elif v!=None:	
            d[k].append(v)
    else:
        if type(v) is list and len(v)>0:
            d[k] = v
        elif v!=None:
            d[k] = [v]
    return d

def notShout(tokens):
    length = len(tokens)
    shout_count = 0.0
    for word in tokens:
        if word.isupper():
            shout_count += 1
    print 'length %d' %length
    print 'shout count %d' %shout_count
    if shout_count/length<.6:
        return True
    else:
        return False

#load global lists of stopwords here
stop = stopwords.words('english')
adhoc_stop = ['RT', 'via', '...']
global_stop = stop + [ts.lower() for ts in adhoc_stop]
all_words = words.words()
punctuation = list(punctuation) + [f+l for f,l in list(permutations(punctuation, 2))]
count = 0
tweet_words = []
for tweet in tweets[100:200]:
    tweet = tweet[0] #keyed tuple from sqlalchemy
    tweet = tweet.strip()
    tweet = tweet.encode('ascii', 'ignore')
    print tweet
    #grab the special text
    hashtags = re.findall(re_hashtag, tweet)
    retweets = re.findall(re_retweets, tweet)
    urls = re.findall(re_urls, tweet)
    mentions = [m for m in re.findall(re_mentions, tweet) if m not in retweets]
    #create filters
    punctless_filter = hashtags + mentions + retweets + punctuation
    punctfull_filter = urls
    url_chars = [(tweet.index(url),len(url)) for url in urls]
    #filter the tweet
    words = [word for word in tweet.split() if word not in punctfull_filter]
    tweet = " ".join(words)
    words = [word for word in wordpunct_tokenize(tweet) if word not in punctless_filter]
    if notShout(words):
        acronyms = [a for a in re.findall(re_acronym, tweet) if a.lower() not in global_stop]
        cap_words = re.findall(re_comp, tweet)
        words = [word.lower() for word in words if word.lower() not in global_stop]
        tweet = " ".join(words)
        #debug
        print '|urls %s' %urls
        print '|hashtags %s' %hashtags
        print '|mentions %s' %mentions
        print '|retweets %s' %retweets
        print '|cap_words %s' %cap_words
        print '|acronyms %s' %acronyms
        print words
        if len(retweets)==0:
            count += 1
            tweet_words.append(words)
            word_count.update(words) #counts
            word_set |= set(words)     #set of words
    #     mention_set |= set(mentions)
    #     retweets_set |= set(retweets)
    else:
        print 'Found a shout!'
    print "----------------"
print count  