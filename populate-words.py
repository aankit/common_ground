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
tweets = db_session.query(Tweet).all()

for t in tweets:
	data = json.loads(t.data)
	search = ParseStatus(data)
	words = search.tweetText().split()
	if(len(t.words)==0):
		for w in words:
		    try:
		        w_obj = db_session.query(Word).filter(Word.word == w).one()
		    except MultipleResultsFound:
		        pass
		    except NoResultFound:
		        if w.lower() not in stop:
			        w_obj = Word(word=w)
			        db_session.add(w_obj)
		    except OperationalError:
			    print 'error'
			    db_session.rollback()
		    t.words.append(w_obj)
		    db_session.commit()
