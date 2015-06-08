import os
import unittest
from flask import Flask
# from tinyErrands import app as application
from tinyErrandsModel import User,Card,Post,Base,followers,UserPostLike
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,orm
from sqlalchemy.orm import sessionmaker,scoped_session
from datetime import datetime, timedelta
import stripe
application = Flask(__name__)


class TestCase(unittest.TestCase):
    def setUp(self):
        application.config['TESTING']=True
        application.config['WTF_CSRF_ENABLED'] = False
        application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admingDa8K2f:Xq4CV8_Br5jU@127.0.0.1:3306/tinyerrands'
        self.application = application.test_client()
        application.config['PROPAGATE_EXCEPTIONS'] =True
        self.engine = create_engine('mysql://admingDa8K2f:Xq4CV8_Br5jU@127.0.0.1:3306/tinyerrands')
        self.connection =self.engine.connect()
        self.transaction = self.connection.begin()
        self.s = scoped_session(sessionmaker())
        self.s(bind=self.connection)
        Base.metadata.create_all(self.engine)
        stripe.api_key = 'sk_test_OM2dp9YnI2w5eNuUKtrxd56g'

        
        
    
    def tearDown(self):
        self.transaction.rollback()
        self.connection.close()
        self.s.remove()

        
        
    def test_make_unique_email(self):
        u = User(name='john', email='johnny@example.com',unhashpassword='mysdl')
        self.s.add(u)
        self.s.commit()
        
        
    def test_follow(self):
        u1 = User(name='john', email='john@example.com',unhashpassword='mysql')
        u2 = User(name='susan', email='susan@example.com',unhashpassword='mysql')
        self.s.add(u1)
        self.s.add(u2)
        self.s.commit()
        self.assertIsNone(u1.unfollow(u2))  
        u = u1.follow(u2)
        self.s.add(u)
        self.s.commit()
        self.assertIsNone(u1.follow(u2))
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().name == 'Susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().name == 'John'
        u = u1.unfollow(u2)
        assert u is not None
        self.s.add(u)
        self.s.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0
        
    def test_follow_posts(self):
         
         u1 = User(name='djibril', email='djibril@example.com',unhashpassword='mypass')
         u2 = User(name='ladji', email='ladji@example.com',unhashpassword='mypass')
         u3 = User(name='hussein', email='hussein@example.com',unhashpassword='mypass')
         u4 = User(name='rohit', email='rohit@example.com',unhashpassword='mypass')
         self.s.add(u1)
         self.s.add(u2)
         self.s.add(u3)
         self.s.add(u4)
         utcnow = datetime.utcnow()
         p1 = Post(body="post from djibril", author=u1, timestamp=utcnow + timedelta(seconds=1))
         p2 = Post(body="post from ladji", author=u2, timestamp=utcnow + timedelta(seconds=2))
         p3 = Post(body="post from hussein", author=u3, timestamp=utcnow + timedelta(seconds=3))
         p4 = Post(body="post from rohit", author=u4, timestamp=utcnow + timedelta(seconds=4))
         self.s.add(p1)
         self.s.add(p2)
         self.s.add(p3)
         self.s.add(p4)
         self.s.commit()
         
         u1.follow(u1)  # djibril follows himself
         u1.follow(u2)  # djibril follows susan
         u1.follow(u4)  # djibril follows david
         u2.follow(u2)  # ladji follows herself
         u2.follow(u3)  # ladji follows mary
         u3.follow(u3)  # hussein follows herself
         u3.follow(u4)  # hussein follows david
         u4.follow(u4)  #rohit follows himself
         
         self.s.add(u1)
         self.s.add(u2)
         self.s.add(u3)
         self.s.add(u4)
         self.s.commit()
         f1 = u1.followed_posts(self.s).all()
         f2 = u2.followed_posts(self.s).all()
         f3 = u3.followed_posts(self.s).all()
         f4 = u4.followed_posts(self.s).all()
         assert len(f2) == 2
         assert len(f3) == 2
         assert len(f4) == 1
         assert f1 == [p4, p2, p1]
         assert f2 == [p3, p2]
         assert f3 == [p4, p3]
         assert f4 == [p4]
    def liking_Post(self):
         u1 = User(name='djibril', email='djibril@example.com', unhashpassword='mypass')
         u2 = User(name='ladji', email='ladji@example.com',unhashpassword='mypass')
         u3 = User(name='hussein', email='hussein@example.com',unhashpassword='mypass')
         u4 = User(name='rohit', email='rohit@example.com',unhashpassword='mypass')
         self.s.add(u1)
         self.s.add(u2)
         self.s.add(u3)
         self.s.add(u4)
         utcnow = datetime.utcnow()
         p1 = Post(body="post from djibril", author=u1, timestamp=utcnow + timedelta(seconds=1))
         p2 = Post(body="post from ladji", author=u2, timestamp=utcnow + timedelta(seconds=2))
         p3 = Post(body="post from hussein", author=u3, timestamp=utcnow + timedelta(seconds=3))
         p4 = Post(body="post from rohit", author=u4, timestamp=utcnow + timedelta(seconds=4))
         self.s.add(p1)
         self.s.add(p2)
         self.s.add(p3)
         self.s.add(p4)
         self.s.commit()
         print p1.get_postedTime()
         u1like = UserPostLike()
         u1like.like(u1,p2,self.s)
         u1like.like(u2,p2,self.s)
         u1like.like(u3,p2,self.s)
         self.s.add(u1like)
         self.s.add(p2)
         self.s.commit()
         assert p2.like_count == 3
    def test_Card(self):
         u1 = User(name='djibril Keita', email='djibril@example.com', unhashpassword='mypass')
         u2 = User(name='ladji Keita', email='ladji@example.com',unhashpassword='mypass')
         u3 = User(name='hussein Keita', email='hussein@example.com',unhashpassword='mypass')
         u4 = User(name='rohit Keita', email='rohit@example.com',unhashpassword='mypass')
         self.s.add(u1)
         self.s.add(u2)
         self.s.add(u3)
         self.s.add(u4)
         c1 = Card(CardNumber='4000000000000077',expYear='2017',expMonth='12',User_id=u1.id)
         c2 = Card(CardNumber='4000056655665556',expYear='2018',expMonth='10',User_id=u2.id)
         self.s.add(c1)
         self.s.add(c2)
         self.s.commit()
         token = stripe.Token.create(
            card={
                "number":c1.CardNumber,
                "exp_month":c1.expMonth,
                "exp_year": c1.expYear,
                },
                )
        
         assert token is not None
         token2 = stripe.Token.create(
            card={
                "number":c2.CardNumber,
                "exp_month":c2.expMonth,
                "exp_year": c2.expYear,
                },
                )
         assert token2 is not None
         stripeAmount = 1000
         charged = stripe.Charge.create(
            description="test.py",
            amount = stripeAmount,
            currency = "usd",
            source= token.id
            )
         assert charged is not None
         recipient = stripe.Recipient.create(
            name =u2.name,
            type ="individual",
            email=u2.email,
            card = token2.id
            )

         transfer= stripe.Transfer.create(
         amount=stripeAmount,
         currency="usd",
         recipient = recipient.id,
         source_transaction = charged.id
         )
         assert transfer is not None
         
         
         
    def truncate(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)


        
         
        
if __name__ == '__main__':
    unittest.main()