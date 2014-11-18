#get user friends

import keys, twitter
from tweetsql.model import Friend
from tweetsql.database import Base, db_session, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

#set up twitter api
twitter_auth = twitter.oauth.OAuth(keys.OAUTH_TOKEN, keys.OAUTH_TOKEN_SECRET, keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
api = twitter.Twitter(auth=twitter_auth)

#let's get 15 screen names that are not in the Friend table

