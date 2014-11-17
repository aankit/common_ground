#!/usr/bin/env python

import json
import twitter
from tweetsql.database import Base, db_session, engine
from tweetsql.model import Tweet, User, Word
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

CONSUMER_KEY = '7fXq6uVQ5agFwdcOIG5zVkIFE'
CONSUMER_SECRET = 'egp1S2RfnRF6TRgqZQhCsaxL2VuppLZBK0q8NXU6rXM7tdKHyp'

OAUTH_TOKEN = '15770482-vQ8gn5MqDUi3bY2teWJL0ioJBsuDlet6MHb4uKWC4'
OAUTH_TOKEN_SECRET = 'cVIEPcLYyZ6YxLOvIcprVF71rYMlUOWW8k7AlKHsUv3ar'

TRACK = 'common core, CCSS, commoncore'

twitter_auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = twitter.TwitterStream(auth=twitter_auth)

statuses = twitter_stream.statuses.filter(track=TRACK)

for t in statuses:
    try:
        print t['text']
    except:
        print 'no text found'
    try:
        u = db_session.query(User).filter_by(uid=str(t['user']['id'])).one()
    except NoResultFound:
        u = User(screen_name=t['user']['screen_name'], uid=t['user']['id'])
        db_session.add(u)
        db_session.commit()

    tw = Tweet(tweet=t['text'], tid=t['id'], user_id=u.id, created_at=t['created_at'], data=json.dumps(t))

    try:
        words = tw.tweet.split()
        for w in words:
            try:
                w_obj = db_session.query(Word).filter(Word.word == w).one()
            except MultipleResultsFound:
                pass
            except NoResultFound:
                w_obj = Word(word=w)
                db_session.add(w_obj)
                db_session.commit()
                tw.words.append(w_obj)
        db_session.add(tw)
        print 'tweet added'
        db_session.commit()
        print 'session committed'
    except OperationalError:
        print 'error'
        db_session.rollback()
