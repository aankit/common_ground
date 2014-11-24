from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from tweetsql.database import Base

hashtag_tweet = Table('hashtag_tweet', Base.metadata,
    Column('hashtag_id', Integer, ForeignKey('hashtag.id'), nullable=False),
    Column('tweet_id', Integer, ForeignKey('tweet.id'), nullable=False))

hashtag_user = Table('hashtag_user', Base.metadata,
    Column('hashtag_id', Integer, ForeignKey('hashtag.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False))

tweet_word = Table('tweet_word', Base.metadata,
    Column('tweet_id', Integer, ForeignKey('tweet.id'), nullable=False),
    Column('word_id', Integer, ForeignKey('word.id'), nullable=False))

class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    tweet = Column(String(300), nullable=False)
    tid = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    #these are the relationships tying the tweet to the user and word tableshtml
    user = relationship('User', backref='tweets', cascade="save-update, merge, delete")
    words = relationship('Word', backref='tweets', secondary=tweet_word)
    
    created_at = Column(String(100), nullable=False)
    data = Column(Text, nullable=False)

    def __repr__(self):
        return '<Tweet {}>'.format(self.tid)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    screen_name = Column(String(100), nullable=False)
    uid = Column(String(50), nullable=False)
    botscore = Column(Integer)

    def __repr__(self):
        return '<User {}>'.format(self.screen_name)

class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    word = Column(String(100), nullable=False)

    def __repr__(self):
        return '<Word {}>'.format(self.word)

class Hashtag(Base):
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True)
    hashtag = Column(String(200), nullable=False)
    users = relationship('User', backref='hashtags', secondary=hashtag_user)
    tweets = relationship('Tweet', backref='hashtags', secondary=hashtag_tweet)

    def __repr__(self):
        return '<Hashtag {}>'.format(self.hashtag)

class Friend(Base):
    __tablename__ = 'friend'
    id = Column(Integer, primary_key=True)
    friend_id = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='friends')

    def __repr__(self):
        return '<Friend {}>'.format(self.friend_id)

class UserData(Base):
    __tablename__='userdata'
    id = Column(Integer, ForeignKey(
        'user.id',  
        ondelete="CASCADE"), 
    primary_key=True)
    description = Column(Text)
    location = Column(String(100))
    geo = Column(Boolean)
    url = Column(String(100))
    utc_offset = Column(Integer)

    def __repr__(self):
        return '<UserData {}>'.format(self.id)

class NoUser(Base):
    __tablename__='nouser'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='deaduser')

    def __repr__(self):
        return '<UserData {}>'.format(self.id)



