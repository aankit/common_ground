#this is all about words
import re, nltk
from string import punctuation, ascii_lowercase
from itertools import permutations
from patterns import *
from nltk.tokenize import wordpunct_tokenize
nltk.data.path.append('./tweetEasy/nltk_data/') #this may need to change depending on when
from nltk.corpus import stopwords
from collections import Counter
from tweetsql.model import Tweet, Hashtag
from tweetsql.database import db_session
import pickle

tweets = db_session.query(Tweet.tweet).all()
db_hashtags = db_session.query(Hashtag.hashtag).all()

print 'db query done'

word_set = set()
word_count = Counter()
wordco = {} #word co-occcurence dictionary

hashtag_set = set([ht[0].lower() for ht in db_hashtags])
hashtag_count = Counter()
hashtagco = {} #hashtag co-occurence dictionary

cap_words_count = Counter()
acronyms_count = Counter()

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
    if length >0:
        shout_count = 0.0
        for word in tokens:
            if word.isupper():
                shout_count += 1
        if shout_count/length<.6:
            return True
        else:
            return False
    else:
        return False

#load global lists of stopwords here
adhoc_stop = ['RT', 'via', '...', 'de', 'amp']
global_stop = stopwords.words('english') + [ts.lower() for ts in adhoc_stop] + list(ascii_lowercase)
punctuation = list(punctuation) + [f+l for f,l in list(permutations(punctuation, 2))]


count = 0
shout_count = 0
tweet_words = []
for tweet in tweets:
    tweet = tweet[0] #keyed tuple from sqlalchemy
    tweet = tweet.strip()
    tweet = tweet.encode('ascii', 'ignore')
    # print tweet
    #grab the special text
    hashtags = re.findall(re_hashtag, tweet)
    retweets = re.findall(re_retweets, tweet)
    urls = re.findall(re_urls, tweet)
    mentions = [m for m in re.findall(re_mentions, tweet) if m not in retweets]
    #create filters
    punctfull_filter = urls #leaving this as such so that I can easliy add filters for 'words' with punctuation
    punctless_filter = hashtags + mentions + retweets + punctuation
    #filter the tweet
    words = [word for word in tweet.split() if word not in punctfull_filter]
    tweet = " ".join(words)
    words = [word for word in wordpunct_tokenize(tweet) if word not in punctless_filter]
    if notShout(words):
        acronyms = [a for a in re.findall(re_acronym, tweet) if a.lower() not in global_stop]
        acronyms_count.update(acronyms)
        cap_words = re.findall(re_comp, tweet)
        cap_words_count.update(cap_words)
        words = [word.lower() for word in words if word.lower() not in global_stop and not word.isdigit()]
        tweet = " ".join(words)
        #debug
        # print '|urls %s' %urls
        # print '|hashtags %s' %hashtags
        # print '|mentions %s' %mentions
        # print '|retweets %s' %retweets
        # print '|cap_words %s' %cap_words
        # print '|acronyms %s' %acronyms
        # print words
        if len(retweets)==0:
            count += 1
            tweet_words.append(words)
            #counts
            word_count.update(words)
            hashtags = [h.lower() for h in re.findall(re_hashtag, tweet)]
            hashtag_count.update(hashtags)
            word_set |= set(words)     #set of words
    #     mention_set |= set(mentions)
    #     retweets_set |= set(retweets)
    else:
        shout_count += 1
    # print "----------------"

print shout_count
print len(word_count)
print word_count.most_common(50)
print cap_words_count.most_common(50)
print acronyms_count.most_common(50)

#let's pickle some things
output_wc = open('word_count.p', 'wb')
output_cp = open('')


# print count
# for k,v in word_count.iteritems():
#     if v==1:
#         print k