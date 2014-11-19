#get user friends

import keys, twitter
from tweetsql.model import Friend, User
from tweetsql.database import Base, db_session, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

#set up twitter api
twitter_auth = twitter.oauth.OAuth(keys.OAUTH_TOKEN, keys.OAUTH_TOKEN_SECRET, keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
api = twitter.Twitter(auth=twitter_auth)

#let's get 15 screen names that are not in the Friend table
got_friends = db_session.query(Friend.user_id).all() #first get all users in the friend table
all_users = db_session.query(User.id).all()

no_friends = [userID for userID in all_users if userID not in got_friends]

for user in no_friends[:15]:
	try:
		screen_name = db_session.query(User.screen_name).filter_by(id=user).one()
		screen_name = screen_name[0].encode('ascii', 'ignore') #get out of the keyed tuple returned by sqlalchemy
	except MultipleResultsFound:
		print 'this is confusing'
		break
	cursor = -1
	friends = []
	while cursor != 0:
		results = api.friends.id(screen_name=screen_name, cursor=cursor)
		cursor = results['next_cursor']
		for friend in results['ids']:
			friends.append(friend)
	for friend in friends:
		f = Friend(friend_id=friend, user_id=user)
		db_session.add(f)
		db_session.commit()


