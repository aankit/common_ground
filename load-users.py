#saving some select user data from twitter

import twitter, keys.lu
from tweetsql.model import UserData, User
from tweetsql.database import Base, db_session, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

#set up twitter api
twitter_auth = twitter.oauth.OAuth(keys.lu.OAUTH_TOKEN, keys.lu.OAUTH_TOKEN_SECRET, keys.lu.CONSUMER_KEY, keys.lu.CONSUMER_SECRET)
api = twitter.Twitter(auth=twitter_auth)

got_data = db_session.query(UserData.user_id).all() #first get all users in the friend table
all_users = db_session.query(User.id, User.uid).all()

no_data = [(pk,uid) for pk,uid in all_users if pk not in got_data]
no_data_100s = [no_data[i:i+99] for i in range(0,len(no_data),100)] #group no_data by 100 for our twitter call
	

for l in no_data_100s[:150]:
	query_string = ''
	for pk,uid in l[:-1]:
		query_string=uid+","
	query_string = query_string + l[-1]
	results = api.users.lookup(user_id=query_string)




