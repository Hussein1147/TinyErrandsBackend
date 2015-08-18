from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,ForeignKey,Integer,BigInteger,String,DateTime,Table
from sqlalchemy.orm import relationship,sessionmaker,mapper,backref
from sqlalchemy.sql import update, insert
from sqlalchemy import create_engine,orm
from werkzeug import generate_password_hash, check_password_hash
import warnings


Base = declarative_base()

followers = Table('followers',
Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.id')),
   Column('followed_id', Integer, ForeignKey('user.id'))
)
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key =True)
    name =Column(String(250),nullable= False)
    email = Column(String(250), unique =True)
    password = Column(String(250))
    posts = relationship('Post', backref='author', lazy='dynamic')
    about_me =Column(String(140))
    last_seen = Column(DateTime)
    followed = relationship('User', backref= backref('followers', lazy='dynamic'), 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               lazy='dynamic')
    def __init__(self, name, email, unhashpassword,about_me=None,last_seen=None):
        self.name = name.title()
        self.email = email.lower()
        self.set_password(unhashpassword)
        self.last_seen=last_seen
        self.about_me = about_me
    def set_password(self, unhashpassword):
        self.password = generate_password_hash(unhashpassword)
    def check_password(self, unhashpassword):
       return check_password_hash(self.password,unhashpassword)
       
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
    def get_followers(self,session):
        return session.query(User.name,User.email).join(followers,followers.c.followed_id == User.id).filter(followers.c.follower_id == self.id).order_by(User.name.asc()).all()
    
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
    def is_following(self,user):
        ## modify
        return self.followed.filter(followers.c.followed_id ==user.id).count() > 0
    def get_myposts(self,session):
        return session.query(Post).filter(Post.user_id == self.id).order_by(Post.timestamp.desc()).all()
        
    def followed_posts(self,session):
        return session.query(Post).join(followers, followers.c.followed_id == Post.user_id).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc()).all()
class Post(Base):
    __tablename__='posts'
    id = Column(Integer, primary_key = True)
    myPost = Column(String(140))
    timestamp = Column(DateTime)
    postedTime = Column(String(40))
    startTime =Column(DateTime(40))
    postedDate = Column(String(40))
    dueDate = Column(Integer)
    user_id = Column(Integer,ForeignKey('user.id'))
    like_count = Column(Integer, default = 0)
    def __init__(self, myPost,timestamp,author,dueDate,startTime,postedDate=None,postedTime=None,like_count=None):
        self.myPost=myPost
        self.timestamp=timestamp
        self.author =author
        self.dueDate =dueDate
        self.startTime = startTime
    
   
   
    
class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer,primary_key=True)
    CardNumber = Column(BigInteger)
    expMonth = Column(Integer)
    expYear = Column(Integer)
    User_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

class UserPostLike(Base):
    __tablename__ = 'likes'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('user.id'))
    post_id = Column(Integer,ForeignKey('posts.id'))
    
    def like(self,user,post,session):
        query = session.query(UserPostLike).filter(UserPostLike.user_id == user.id).filter(UserPostLike.post_id == post.id).all()
        if len(query) == 0:
            ###
            # THIS IS NOT AN ERROR
            session.execute(UserPostLike.__table__.insert(),{"user_id": user.id, "post_id": post.id})
            likes = post.like_count
            session.query(Post).filter(Post.id ==post.id).update({"like_count": likes + 1})
           
        
   
#
#
#change ip address when done testing please!!!!!!!!
#
#
#
engine = create_engine('mysql://admingDa8K2f:Xq4CV8_Br5jU@127.6.142.132:3306/tinyerrands'
s = sessionmaker()
s.configure(bind=engine)
Base.metadata.create_all(engine)
S = s()
Base.metadata.create_all(engine)