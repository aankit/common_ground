#saving some select user data from twitter

import twitter, keys.lu, sys
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
#group no_data by 100 for our twitter call
no_data_100s = [no_data[i:i+99] for i in range(0,len(no_data),100)] 

def get_rate_limit(t, data='remaining'):
    limit = t.application.rate_limit_status()
    return limit['resources']['users']['/users/lookup'][data]

if get_rate_limit(t=api, data='remaining')==0:
	print 'rate limit hit'
	print 'try again at %d' %get_rate_limit(t=api, data='reset')
	sys.exit()

for l in no_data_100s:
	if get_rate_limit(t=api, data='remaining')==0:
		print 'rate limit hit'
		print 'try again at %d' %get_rate_limit(t=api, data='reset')
		break
	query_string = ''
	for pk,uid in l[:-1]:
		query_string=uid+","
	query_string = query_string + l[-1]
	results = api.users.lookup(user_id=query_string)[0]
	ud = UserData(description = results['description'], location = results['location'],
    geo = results['geo_enabled'], url = results['url'], utc_offset = results['utc_offset'])
    db_session.add(ud)
    df_session.commit()




