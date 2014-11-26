#!/Users/Aankit/Documents/SocialDataAnalysis/commonCore/bin/python

import twitter, keys.lu, keys.lf1, keys.lf2, keys.ls, sys, twitter, json
from tweetsql.model import Friend, User, NoUser
from tweetsql.database import Base, db_session, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import distinct

keys = [keys.lu, keys.lf1, keys.lf2, keys.ls]

def get_rate_limit(t, data='remaining'):
    limit = t.application.rate_limit_status()
    return limit['resources']['friends']['/friends/ids'][data]

def get_clean_key():
	maxRemaining = 0
	winner = ''
	for k in keys:
		twitter_auth = twitter.oauth.OAuth(k.OAUTH_TOKEN, k.OAUTH_TOKEN_SECRET, k.CONSUMER_KEY, k.CONSUMER_SECRET)
		api = twitter.Twitter(auth=twitter_auth)
		remaining = get_rate_limit(t=api)
		if remaining > maxRemaining:
			maxRemaining = remaining
			winner = k
	return winner

#set up twitter api
clean_key = get_clean_key()
twitter_auth = twitter.oauth.OAuth(clean_key.OAUTH_TOKEN, clean_key.OAUTH_TOKEN_SECRET, 
	clean_key.CONSUMER_KEY, clean_key.CONSUMER_SECRET)
api = twitter.Twitter(auth=twitter_auth)

if get_rate_limit(t=api, data='remaining')==0:
	print 'rate limit hit'
	print 'try again at %d' %get_rate_limit(t=api, data='reset')
	sys.exit()


#let's get 15 screen names that are not in the Friend table
got_friends = db_session.query(distinct(Friend.user_id)).all() #first get all users in the friend table
got_friends = [t[0] for t in got_friends]
dead_users = db_session.query(NoUser.user_id).all()
dead_users = [t[0] for t in dead_users]
all_users = db_session.query(User.id, User.uid).all()
all_users = [(pk,uid) for pk,uid in all_users if pk not in dead_users] #filter out dead users
no_friends = [(pk,uid) for pk,uid in all_users if pk not in got_friends] #get rid of people with friends

# rate_limit = 15
# requests = 0
print no_friends[:15]
for pk,uid in no_friends:
	cursor = -1
	friends = []
	if get_rate_limit(t=api, data='remaining')==0:
		print 'rate limit hit'
		print 'try again at %d' %get_rate_limit(t=api, data='reset')
		break
	got_an_error = False
	while cursor != 0:
		try:
			results = api.friends.ids(user_id=uid, cursor=cursor) #get list of friends (500 at a time)
			cursor = results['next_cursor'] #next cursor
			for friend in results['ids']: #save to list
				friends.append(friend)
		except Exception,e:
			got_an_error = True
			error = json.loads(e.response_data)
			try:
				error = error['error']
			except KeyError:
				error = error['errors'][0]
			print error
			print 'User protected or doesn\'t exist'
			du = NoUser(user_id=pk)
			db_session.add(du)
			db_session.commit()
			print 'dead user committed'
			break

	if len(friends)==0 and not got_an_error:
		f = Friend(friend_id=0, user_id=pk)
		db_session.add(f)
		db_session.commit()
		print "not following anyone?"
	else:
		for friend in friends:
			try:
				f = Friend(friend_id=friend, user_id=pk)
				db_session.add(f)
				db_session.commit()
			except:
				print 'error'
				db_session.rollback()

