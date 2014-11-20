#saving some select user data from twitter

import twitter, keys.lu
from tweetsql.model import Friend, User
from tweetsql.database import Base, db_session, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

#set up twitter api
twitter_auth = twitter.oauth.OAuth(keys.lu.OAUTH_TOKEN, keys.lu.OAUTH_TOKEN_SECRET, keys.lu.CONSUMER_KEY, keys.lu.CONSUMER_SECRET)
api = twitter.Twitter(auth=twitter_auth)




