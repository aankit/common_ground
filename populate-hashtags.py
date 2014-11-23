import json
from tweetEasy.tweetEasy import ParseStatus
from tweetsql.database import db_session as sesh
from tweetsql.model import Hashtag, Tweet

for t in sesh.query(Tweet).all()[:10]:
	data = json.loads(t.data)
	search = ParseStatus(data)
	for hashtag in search.hashtags():
		ht = Hashtag(hashtag=hashtag)
		sesh.add(ht)
		sesh.commit()

