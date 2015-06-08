from flask import Flask
import sys,os
import stripe
import unicodedata
from flask import Flask,request,json,Response,jsonify
from sqlalchemy import create_engine,update
from sqlalchemy.orm import sessionmaker,scoped_session
from tinyErrandsModel import User,Card,Post,UserPostLike
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,orm,exc
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

Base = declarative_base()
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] =True
stripe.api_key = 'sk_test_OM2dp9YnI2w5eNuUKtrxd56g'
engine = create_engine('mysql://admingDa8K2f:Xq4CV8_Br5jU@127.6.142.132:3306/tinyerrands')

s = sessionmaker()
s.configure(bind=engine)
Base.metadata.create_all(engine)
session = s()
def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
          return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"
    
def validate_user(pwdhash,password):
        if check_password_hash(pwdhash,password):
            return True
        else:
            return False
def get_user_by_email(value):
    try:
        user = session.query(User).filter(User.email == value).first()
        return user
    except exc.NoResultFound:
        return None
def get_user_by_id(value):
    try:
        user = session.query(User).filter(User.id == int(value)).first()
        return user
    except exc.NoResultFound:
        return None      
def get_post_by_id(value):
    try:
        post = session.query(Post).filter(Post.id == value).first()
        return post
    except exc, e:
        print "Some Error Happen durring quering post see exception"
        print e
        return None
@app.route('/')
@app.route('/createUser',methods=['Post'])
def createUser():
    data = request.get_json(force=True)
    userName = unicodedata.normalize('NFKD', data['userName']).encode('ascii','ignore')
    #must validate email and passwords 
    #
    ####
    userPassword = unicodedata.normalize('NFKD', data['userPassword']).encode('ascii','ignore')
    userEmail=unicodedata.normalize('NFKD', data['userEmail']).encode('ascii','ignore')
    userCardNumber=unicodedata.normalize('NFKD', data['userCardNumber']).encode('ascii','ignore')
    userExpMonth=unicodedata.normalize('NFKD', data['userExpMonth']).encode('ascii','ignore')
    userExpYear=unicodedata.normalize('NFKD', data['userExpYear']).encode('ascii','ignore')
    try:
        if session.query(User).filter(User.email == userEmail).first() is  None: 
            new_person =User(name=userName,email=userEmail,unhashpassword=userPassword)
            session.add(new_person)
            session.commit()
    #create and add User Card
            new_person_card = Card(CardNumber=userCardNumber,expMonth=userExpMonth,expYear=userExpYear,user=new_person)
    
            session.add(new_person_card)
            session.commit()
            return Response(json.dumps("Success, Created!"))
        else:
            return Response(json.dumps("User email is taken!"))
            
    except exc.IntegrityError, e:
        session.rollback()
        return Response(e)
    except exc.InvalidRequestError, e:
        session.rollback()
        return Response(e)
        
@app.route('/follow',methods=['POST'])
def follow_user():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    userFollowedEmail =unicodedata.normalize('NFKD', data['userFollowedEmail']).encode('ascii','ignore')
    currentUser_obj = get_user_by_email(currentUserEmail)
    userFollowed_obj = get_user_by_email(userFollowedEmail)

    if currentUser_obj.is_following(userFollowed_obj) is not True:
        u = currentUser_obj.follow(userFollowed_obj)
        session.add(u)
        session.commit()
        response = "Now Following" +" "+ userFollowed_obj.name
        return Response(json.dumps(response))
    else:
        response = "This user is already being followed"
        return Response(json.dumps(response))


    
@app.route('/get_followers',methods=['POST'])
def get_followers():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    currentUser_obj = get_user_by_email(currentUserEmail)
    followers = currentUser_obj.get_followers(session)
    return Response(json.dumps(followers))

    
@app.route('/add_post',methods =['POST'])
def add_post():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    post = unicodedata.normalize('NFKD', data['myPost']).encode('ascii','ignore')
    utcnow = datetime.now()
    currentUser_obj = get_user_by_email(currentUserEmail)
    p1 = Post(body=post, author=currentUser_obj, timestamp=utcnow)
    session.add(p1)
    session.commit()
    return Response(json.dumps("Ok"))

   
@app.route('/get_followed_post',methods =['POST'])
def get_followed_post():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    currentUser_obj = get_user_by_email(currentUserEmail)
    posts = currentUser_obj.followed_posts(session)
    response = []
    for post in posts:
        post.postedTime =  pretty_date(post.timestamp)
        del post.__dict__['_sa_instance_state']
        del post.__dict__['timestamp']
        response.append(post.__dict__)
    return Response(json.dumps(response))
    
    
    
@app.route('/transfer', methods=["POST"])
def transfer():
    # register(APPLICATION_ID,REST_API_KEY)
    data = request.get_json(force=True)
    
    currentUserEmail= unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    recipientEmail =unicodedata.normalize('NFKD', data['recipientEmail']).encode('ascii','ignore')
    stripeAmount =unicodedata.normalize('NFKD', data['amount']).encode('ascii','ignore')
    stripeCurrency =unicodedata.normalize('NFKD', data['stripeCurrency']).encode('ascii','ignore')
    stripeDescription=unicodedata.normalize('NFKD', data['stripeDescription']).encode('ascii','ignore')
    currentUser_obj = session.query(User).filter(User.email == currentUserEmail).one()
    currentUserCard_obj = session.query(Card).filter(Card.user ==currentUser_obj).one()
    recipient_obj = session.query(User).filter(User.email == recipientEmail).one()
    recipientCard_obj = session.query(Card).filter(Card.user ==recipient_obj).one()
    print recipient_obj.name

    try:
        token = stripe.Token.create(
            card={
                "number":recipientCard_obj.CardNumber,
                "exp_month":recipientCard_obj.expMonth,
                "exp_year": recipientCard_obj.expYear,
                },
                )
        
        recipient = stripe.Recipient.create(
            name =recipient_obj.name,
            type ="individual",
            email=recipientEmail,
            card = token.id
            )
        token2 = stripe.Token.create(
            card={
                "number":currentUserCard_obj.CardNumber,
                "exp_month":currentUserCard_obj.expMonth,
                "exp_year": currentUserCard_obj.expYear,
                },
                )
        charged = stripe.Charge.create(
            description=stripeDescription,
            amount = stripeAmount,
            currency = stripeCurrency,
            source= token2.id
            )

        transfer= stripe.Transfer.create(
        amount=stripeAmount,
        currency=stripeCurrency,
        recipient = recipient.id,
        source_transaction= charged.id
        )
        return Response(json.dumps(transfer))

    except stripe.error.CardError, e:
        body = e.json_body
        err  = body['error']
        return Response(json.dumps(err))
    except stripe.error.InvalidRequestError, e:
         body = e.json_body
         err  = body['error']
         return Response(json.dumps(err))
  
@app.route('/like_post',methods= ["POST"])

def like_post():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    postId = unicodedata.normalize('NFKD', data['postId']).encode('ascii','ignore')
    try:
        currentUser_obj = get_user_by_email(currentUserEmail)
        post_obj = get_post_by_id(postId)
        userPost = UserPostLike()
        userPost.like(currentUser_obj,post_obj,session)
        session.add(userPost)
        session.add(post_obj)
        session.commit()
        response = {"id":post_obj.id,"like_count": post_obj.like_count}
        return Response(json.dumps(response))
    except exc.InvalidRequestError,e:
        
        Response(e)
        return None   
    
    
    
@app.route('/hello')
def index():
    return "Hello from OpenShift"

 
if __name__ == '__main__':
    app.run()