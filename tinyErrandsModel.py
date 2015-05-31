from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,ForeignKey,Integer,BigInteger,String,DateTime,Table
from sqlalchemy.orm import relationship,sessionmaker,mapper,backref
from sqlalchemy.sql import update, insert
from sqlalchemy import create_engine,orm



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
    password =Column(String(250))
    posts = relationship('Post', backref='author', lazy='dynamic')
    about_me =Column(String(140))
    last_seen = Column(DateTime)
    followed = relationship('User', backref= backref('followers', lazy='dynamic'), 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               lazy='dynamic')
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id ==user.id).count() > 0
        
    def followed_posts(self,session):
        return session.query(Post).join(followers, followers.c.followed_id == Post.user_id).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())
class Post(Base):
    __tablename__='posts'
    id = Column(Integer, primary_key = True)
    body = Column(String(140))
    timestamp = Column(DateTime)
    user_id = Column(Integer,ForeignKey('user.id'))
    like_count = Column(Integer, default = 0)
    
class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer,primary_key=True)
    CardNumber = Column(BigInteger)
    expMonth = Column(Integer)
    expYear = Column(Integer)
    cvc = Column(Integer)
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
            i = insert(UserPostLike)
            i = i.values({"user_id": user.id, "post_id": post.id})
            session.execute(i)
            likes = post.like_count
            session.query(Post).filter(Post.id ==post.id).update({"like_count": likes + 1})
           
        
   
#
#
#change ip address when done testing please!!!!!!!!
#
#
#
engine = create_engine('mysql://admingDa8K2f:Xq4CV8_Br5jU@127.0.0.1:3306/tinyerrands')
s = sessionmaker()
s.configure(bind=engine)
Base.metadata.create_all(engine)
S = s()
Base.metadata.create_all(engine)