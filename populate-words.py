import json
import nltk
from nltk.tokenize import wordpunct_tokenize
nltk.data.path.append('./tweetEasy/nltk_data/') #this may need to change depending on when
from nltk.corpus import stopwords
from tweetEasy.tweetEasy import ParseStatus
from tweetsql.database import db_session
from tweetsql.model import Hashtag, Tweet, Word, User
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

stop = stopwords.words('english')
tweets = db_session.query(Tweet).all()
tweet_words = [t.id for t in db_session.query(Tweet).join(Tweet.words).all()]
tweets = [t for t in tweets if t.id not in tweet_words]

words = db_session.query(Word).all()
all_words = []
tweet_word_dict = {}

count = 0
for t in tweets:
	data = json.loads(t.data)
	search = ParseStatus(data)
	words = wordpunct_tokenize(search.tweetText())
	print len(words)
	count += 1
print count

# 	for w in words:
# 		if w.lower() not in stop:
# 			w_obj = Word(word=w)
# 			db_session.add(w_obj)
# 			t.words.append(w_obj)
# 	db_session.commit()
# 	print 'words committed'
