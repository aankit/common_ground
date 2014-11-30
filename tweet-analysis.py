from tweetsql.model import Tweet, Hashtag
from tweetsql.database import db_session

tweets = db_session.query(Tweet.tweet).filter(Tweet.id<500).all()
db_hashtags = db_session.query(Hashtag.hashtag).all()