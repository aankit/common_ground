#!/Users/Aankit/Documents/SocialDataAnalysis/commonCore/bin/python

import keys.lf1, keys.lf2, twitter, sys, json
from tweetsql.model import Friend, User, NoUser
from tweetsql.database import Base, db_session, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import distinct

f = open('/Users/Aankit/Documents/SocialDataAnalysis/common_core/toggle', 'r')
whichKey = f.read(1)
whichKey = int(whichKey)
f.close()

def toggleKey(newKey):
	f = open('/Users/Aankit/Documents/SocialDataAnalysis/common_core/toggle', 'w')
	f.write(newKey)
	f.close

def get_rate_limit(t, data='remaining'):
    limit = t.application.rate_limit_status()
    return limit['resources']['friends']['/friends/ids'][data]

#set up twitter api, use this toggle to cut the rate limiting in half
if whichKey:
	toggleKey('0')
	print 'first key'
	twitter_auth = twitter.oauth.OAuth(keys.lf1.OAUTH_TOKEN, keys.lf1.OAUTH_TOKEN_SECRET, keys.lf1.CONSUMER_KEY, keys.lf1.CONSUMER_SECRET)
else:
	toggleKey('1')
	print 'second key'
	twitter_auth = twitter.oauth.OAuth(keys.lf2.OAUTH_TOKEN, keys.lf2.OAUTH_TOKEN_SECRET, keys.lf2.CONSUMER_KEY, keys.lf2.CONSUMER_SECRET)
	

api = twitter.Twitter(auth=twitter_auth)

if get_rate_limit(t=api, data='remaining')==0:
	print 'rate limit hit'
	print 'try again at %d' %get_rate_limit(t=api, data='reset')
	sys.exit()


#let's get 15 screen names that are not in the Friend table
got_friends = db_session.query(distinct(Friend.user_id)).all() #first get all users in the friend table
got_friends = [t[0] for t in got_friends]
all_users = db_session.query(User.id, User.uid).all()
dead_users = db_session.query(NoUser.user_id).all()
all_users = [(pk,uid) for pk,uid in all_users if pk not in dead_users] #filter out dead users
no_friends = [(pk,uid) for pk,uid in all_users if pk not in got_friends] #get rid of 

# rate_limit = 15
# requests = 0

for pk,uid in no_friends:
	cursor = -1
	friends = []
	if get_rate_limit(t=api, data='remaining')==0:
		print 'rate limit hit'
		print 'try again at %d' %get_rate_limit(t=api, data='reset')
		break
	while cursor != 0:
		try:
			results = api.friends.ids(user_id=uid, cursor=cursor) #get list of friends (500 at a time)
			cursor = results['next_cursor'] #next cursor
			for friend in results['ids']: #save to list
				friends.append(friend)
		except Exception,e:
			error = json.loads(e.response_data)
			print type(error)
			print 'User protected or doesn\'t exist'
			du = NoUser(user_id=pk)
			db_session.add(du)
			db_session.commit()
			print 'dead user committed'
			break

	print 'got some friends'
	for friend in friends:
		try:
			f = Friend(friend_id=friend, user_id=pk)
			db_session.add(f)
			db_session.commit()
		except OperationalError:
			print 'error'
			db_session.rollback()

