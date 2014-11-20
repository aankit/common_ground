#!/Users/Aankit/Documents/SocialDataAnalysis/commonCore/bin/python

import keys.lf1, keys.lf2, twitter
from tweetsql.model import Friend, User, NoUser
from tweetsql.database import Base, db_session, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import distinct

f = open('/Users/Aankit/Documents/SocialDataAnalysis/common_core/toggle', 'r')
whichKey = int(f.read(1))
f.close()

def toggleKey(newKey):
	f = open('./toggle', 'w')
	f.write(newKey)
	f.close

#set up twitter api, use this toggle to cut the rate limiting in half
if whichKey:
	twitter_auth = twitter.oauth.OAuth(keys.lf1.OAUTH_TOKEN, keys.lf1.OAUTH_TOKEN_SECRET, 
		keys.lf1.CONSUMER_KEY, keys.lf1.CONSUMER_SECRET)
	toggleKey('0')
else:
	twitter_auth = twitter.oauth.OAuth(keys.lf2.OAUTH_TOKEN, keys.lf2.OAUTH_TOKEN_SECRET, keys.lf2.CONSUMER_KEY, 
		keys.lf2.CONSUMER_SECRET)
	toggleKey('1')

api = twitter.Twitter(auth=twitter_auth)

#let's get 15 screen names that are not in the Friend table
got_friends = db_session.query(distinct(Friend.user_id)).all() #first get all users in the friend table
got_friends = [t[0] for t in got_friends]
all_users = db_session.query(User.id, User.uid).all()
dead_users = db_session.query(NoUser.user_id).all()
all_users = [(pk,uid) for pk,uid in all_users if pk not in dead_users] #filter out dead users
no_friends = [(pk,uid) for pk,uid in all_users if pk not in got_friends] #get rid of 

for pk,uid in no_friends[:15]:
	cursor = -1
	friends = []
	while cursor != 0:
		try:
			results = api.friends.ids(user_id=uid, cursor=cursor) #get list of friends (500 at a time)
			cursor = results['next_cursor'] #next cursor
			for friend in results['ids']: #save to list
				friends.append(friend)
		except:
			print 'User didn\'t exist'
			du = NoUser(user_id=pk)
			db_session.add(du)
			db_session.commit()
			print 'dead user committed'
			break

	for friend in friends:
		f = Friend(friend_id=friend, user_id=pk)
		db_session.add(f)
		db_session.commit()

