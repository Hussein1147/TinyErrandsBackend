from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,ForeignKey,Integer,BigInteger,String,DateTime,Table
from sqlalchemy.orm import relationship,sessionmaker,mapper,backref
from sqlalchemy import create_engine,orm



Base = declarative_base()
followers = Table('followers',
    Column('follower_id', Integer, ForeignKey('user.id')),
   Column('followed_id', Integer, ForeignKey('user.id'))
)
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key =True)
    name =Column(String(250),nullable= False)
    email = Column(String(250))
    password =Column(String(250))
    posts = relationship('Post', backref='author', lazy='dynamic')
    about_me =Column(String(140))
    last_seen = Column(DateTime)
    followed = relationship('User', backref= backref('followers', lazy='dynamic'), 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               lazy='dynamic')

class Post(Base):
    __tablename__='posts'
    id = Column(Integer, primary_key = True)
    body = Column(String(140))
    timestamp = Column(DateTime)
    user_id = Column(Integer,ForeignKey('user.id'))

class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer,primary_key=True)
    CardNumber = Column(BigInteger)
    expMonth = Column(Integer)
    expYear = Column(Integer)
    cvc = Column(Integer)
    User_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)
    
engine = create_engine('mysql://admingDa8K2f:Xq4CV8_Br5jU@127.6.142.132:3306/tinyerrands')
Base.metadata.create_all(engine)