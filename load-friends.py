#!/Users/Aankit/Documents/SocialDataAnalysis/commonCore/bin/python

import keys.lf1, twitter
from tweetsql.model import Friend, User
from tweetsql.database import Base, db_session, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

f = open('/Users/Aankit/Documents/SocialDataAnalysis/common_core/toggle', 'r')
whichKey = int(f.read(1))
f.close()

def toggleKey(newKey):
	f = open('./toggle', 'w')
	f.write(newKey)
	f.close

#set up twitter api
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
got_friends = db_session.query(Friend.user_id).all() #first get all users in the friend table
all_users = db_session.query(User.id, User.uid).all()

no_friends = [pk, uid for pk, uid in all_users if pk not in got_friends]

for pk, uid in no_friends[:15]:
	cursor = -1
	friends = []
	while cursor != 0:
		try:
			results = api.friends.ids(user_id=uid, cursor=cursor)
			cursor = results['next_cursor']
			for friend in results['ids']:
				friends.append(friend)
		except:
			print 'User didn\'t exist'
			# db_session.query(User).filter_by(id=user).delete()
			# db_session.commit()
			break

	for friend in friends:
		f = Friend(friend_id=friend, user_id=pk)
		db_session.add(f)
		db_session.commit()


