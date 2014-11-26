#!/Users/Aankit/Documents/SocialDataAnalysis/commonCore/bin/python

import json
import twitter, keys.lu
from tweetsql.database import Base, db_session, engine
from tweetsql.model import Tweet, User, Word, Hashtag
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from tweetEasy.tweetEasy import ParseStatus

TRACK = 'common core, CCSS, commoncore'

twitter_auth = twitter.oauth.OAuth(keys.lu.OAUTH_TOKEN, keys.lu.OAUTH_TOKEN_SECRET,
                           keys.lu.CONSUMER_KEY, keys.lu.CONSUMER_SECRET)

twitter_stream = twitter.TwitterStream(auth=twitter_auth)

statuses = twitter_stream.statuses.filter(track=TRACK)


for t in statuses:
    #add user
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
        print 'user committed'


    #add tweet
    tw = Tweet(tweet=t['text'], tid=t['id'], user_id=u.id, created_at=t['created_at'], data=json.dumps(t))
    db_session.add(tw)
    db_session.commit()
    print 'tweet commited'
    
    #add hashtag
    search = ParseStatus(t)
    hashtags = search.hashtags
    if len(tw.hashtags)==0 and len(hashtags)>0:
        print hashtags
        for h in hashtags:
            try:
                h_obj = db_session.query(Hashtag).filter(Hashtag.hashtag == h).one()            
            except MultipleResultsFound:
                pass
            except NoResultFound:   
                h_obj = Hashtag(hashtag=h)
                db_session.add(h_obj)
                print 'hashtag added'
            except OperationalError:
                print 'error'
                db_session.rollback()
            #add the relationship between h_obj and tweets
            tw.hashtags.append(h_obj)
            u.hashtags.append(h_obj)
            print 'hashtag assoc added'
        db_session.commit()
        print 'hashtag committed'

    # #add words
    # try:
    #     words = tw.tweet.split()
    #     for w in words:
    #         try:
    #             w_obj = db_session.query(Word).filter(Word.word == w).one()
    #         except MultipleResultsFound:
    #             pass
    #         except NoResultFound:
    #             w_obj = Word(word=w)
    #             db_session.add(w_obj)
    #             db_session.commit()
    #         tw.words.append(w_obj)
    #     db_session.commit()
    #     print 'words added'
    # except OperationalError:
    #     print 'error'
    #     db_session.rollback()

    # #add user data


