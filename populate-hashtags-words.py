import json
from tweetEasy.tweetEasy import ParseStatus
from tweetsql.database import db_session
from tweetsql.model import Hashtag, Tweet, Word, User
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

for t, u in db_session.query(Tweet, User).join(Tweet.user).all():
	data = json.loads(t.data)
	search = ParseStatus(data)
	hashtags = search.hashtags()
	print u.screen_name
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
		if t not in h_obj.tweets:
			h_obj.tweets.append(t)
		if u not in h_obj.users:
			h_obj.users.append(u)
		db_session.commit()

		
	words = search.tweetText().split()
	for w in words:
	    try:
	        w_obj = db_session.query(Word).filter(Word.word == w).one()
	    except MultipleResultsFound:
	        pass
	    except NoResultFound:
	        w_obj = Word(word=w)
	        db_session.add(w_obj)
	    except OperationalError:
		    print 'error'
		    db_session.rollback()
	    if w_obj not in t.words:
	    	t.words.append(w_obj)
	    db_session.commit()





