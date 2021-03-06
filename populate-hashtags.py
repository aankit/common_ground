import json
import nltk 
nltk.data.path.append('./tweetEasy/nltk_data/') #this may need to change depending on when
from nltk.corpus import stopwords
from tweetEasy.tweetEasy import ParseStatus
from tweetsql.database import db_session
from tweetsql.model import Hashtag, Tweet, Word, User
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

stop = stopwords.words('english')
tweets_users = db_session.query(Tweet, User).join(Tweet.user).all()

for t, u in tweets_users:
	data = json.loads(t.data)
	search = ParseStatus(data)
	if(len(t.hashtags)==0):
		hashtags = search.hashtags
		for h in hashtags:
			try:
				h_obj = db_session.query(Hashtag).filter(Hashtag.hashtag == h).one()			
			except MultipleResultsFound:
				pass
			except NoResultFound:	
				h_obj = Hashtag(hashtag=h)
				db_session.add(h_obj)
			except OperationalError:
			    print 'error'
			    db_session.rollback()
			#add the relationship between h_obj and tweets
			t.hashtags.append(h_obj)
			u.hashtags.append(h_obj)
			db_session.commit()




