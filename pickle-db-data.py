from tweetsql.model import Tweet, Hashtag, User
from tweetsql.database import db_session
import pickle

def pickleIt(data, fname):
	output = open(fname, 'wb')
	pickle.dump(data, output)

try:
	f = open('user_tweet.p', 'rb')
except:
	tweets = db_session.query(User.id, Tweet.tweet).join(Tweet.user).all()
	pickleIt(tweets, 'user_tweet.p')

try:
	f = open('user_hashtag.p', 'rb')
except:
	hashtags = db_session.query(User.id, Hashtag.hashtag).join(Hashtag.user).all()
	pickleIt(hashtags, 'user_hashtag.p')

