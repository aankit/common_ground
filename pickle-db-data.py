from tweetsql.model import Tweet, Hashtag, User, Friend
from tweetsql.database import db_session
import pickle
from collections import Counter

def pickleIt(data, fname):
	output = open(fname, 'wb')
	pickle.dump(data, output)
	output.close()
	
try:
	f = open('user_tweet.p', 'rb')
	f.close()
except:
	tweets = db_session.query(User.screen_name, Tweet.id, Tweet.tweet).join(Tweet.user).all()
	pickleIt(tweets, 'user_tweet.p')

try:
	f = open('user_hashtag.p', 'rb')
except:
	hashtags = db_session.query(User.screen_name, Hashtag.hashtag).join(Hashtag.users).all()
	pickleIt(hashtags, 'user_hashtag.p')

try:
	f = open('all_user_friends.p', 'rb')
except:
	users = db_session.query(User.id, Tweet.id).join(Tweet.user).all()
	print 'users retrieved'
	tweet_counter = Counter()
	tweet_counter.update([uid for uid, tid in users])
	top_users = set([u for u, t in tweet_counter.items() if tweet_counter[t]>2])
	top_user_friends = set()
	for obj in db_session.query(User.uid, Friend.friend_id)\
		.join(Friend.user)\
		.filter(Friend.user_id.in_(top_users)).yield_per(100):
			print 'got next'
			top_user_friends |= set(obj)
	print 'done with queries'
	pickleIt(top_user_friends, 'all_user_friends.p')
