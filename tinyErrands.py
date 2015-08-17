from flask import Flask,jsonify
import sys,os
import stripe
import unicodedata
from flask import Flask,request,json,Response,jsonify
from sqlalchemy import create_engine,update
from sqlalchemy.orm import sessionmaker,scoped_session
from tinyErrandsModel import User,Card,Post,UserPostLike
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,orm
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError,InvalidRequestError
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
    
def pretty_due(start,interval):
    
    now = datetime.now()
    f = (Interval) - (now - start)
    if f < 60:
        return 'Due in' + f + 'minutes'
   
    elif f == 60:
        return 'Due in 1 hour'
    
    elif 60 <  f < 1440:
        time = f/float(60)
        hours = int(time)
        minutes = int(60 * (time - int(time)))
        return 'Due in ' + hours + ' hours and ' + minutes + ' minutes'
    
    elif f == 1440:
        return 'Due in 1 day'
    
    elif 1440 < f < 1080:
        time = f/1440
        days = int(time)
        hours = int(24 * (time - int(time)))
        return 'Due in ' + days + ' days and ' + hours + ' hours'
    
    elif f == 1080:
        return 'Due in 1 week'
    
    elif  1080 < f < 40320:
        time = f/1080
        weeks = int(time)
        days = int (7 * (time - int(time)))
        return 'Due in '+ weeks + ' weeks and' + days + ' days'
    
    elif f == 40320:
        return 'Due in 1 month'
    
    elif 40320 < f < 483840:
        time = f/40320
        months = int(time)
        weeks = int(4 * (time - int(time)))
        return 'Due in ' + months + ' months and' + weeks + ' weeks'
    
    elif f == 483840:
        return 'Due in 1 year'

    elif  483820 < f < 2419100:
        time = f/483820
        years = int(time)
        months = int(12 * (time - int(time)))
        return 'Due in ' + years + ' years and' + months + ' months'

    
def validate_user(pwdhash,password):
        if check_password_hash(pwdhash,password):
            return True
        else:
            return False
def get_user_by_email(value,new_session):
    try:
        user = new_session.query(User).filter(User.email == value).one()
        return user
    except NoResultFound:
        print "No result found"
        return None
def get_user_by_id(value):
    try:
        user = session.query(User).filter(User.id == int(value)).first()
        return user
    except exc.NoResultFound:
        return None      
def get_post_by_id(value, get_session):
    try:
        post = get_session.query(Post).filter(Post.id == value).first()
        return post
    except NoResultFound, e:
        print "Some Error Happen durring quering post see exception"
        print e
        return None
##
# THIS IS NOT THE FINAL IMPL OF GET_ALL_USERS
##
@app.route('/get_All_Users', methods = ["POST"])
def get_all_users():
    data = request.get_json(force=True)
    userEmail=unicodedata.normalize('NFKD', data['userEmail']).encode('ascii','ignore')
    new_Session=s()
    if get_user_by_email(userEmail,new_Session) is not None:
        response = []
        all_Users = new_Session.query(User.name,User.email).all()
        for user in all_Users:
            del user.__dict__["_labels"]
            response.append(user.__dict__)
        return jsonify(success=True,data=response)
    else:
        error="Some error occured"
        return jsonify(success=False,data=error)
    

@app.route('/add_Card',methods=['Post'])
def addCard():
    data = request.get_json(force=True)
    #must validate email and passwords 
    #
    ####
    userEmail=unicodedata.normalize('NFKD', data['userEmail']).encode('ascii','ignore')
    userCardNumber=unicodedata.normalize('NFKD', data['userCardNumber']).encode('ascii','ignore')
    userExpMonth=unicodedata.normalize('NFKD', data['userExpMonth']).encode('ascii','ignore')
    userExpYear=unicodedata.normalize('NFKD', data['userExpYear']).encode('ascii','ignore')
    try:    
            new_Card_Session =s()
            person =get_user_by_email(userEmail,new_Card_Session)
            #create and add User Card
            new_card = Card(CardNumber=userCardNumber,expMonth=userExpMonth,expYear=userExpYear,user=person)
    
            new_Card_Session.add(new_card)
            new_Card_Session.commit()
            return jsonify(
        success = True,
        data = {
            'msg': 'Success!! created User!',
        }
    )
        
    except IntegrityError, e:
        session.rollback()
        return Response(e)
    except InvalidRequestError, e:
        session.rollback()
        return Response(e)
        
@app.route('/createUser',methods=['Post'])
def createUser():
    data = request.get_json(force=True)
    userName = unicodedata.normalize('NFKD', data['userName']).encode('ascii','ignore')
    #must validate email and passwords 
    #
    ####
    userPassword = unicodedata.normalize('NFKD', data['userPassword']).encode('ascii','ignore')
    userEmail=unicodedata.normalize('NFKD', data['userEmail']).encode('ascii','ignore')
    # userCardNumber=unicodedata.normalize('NFKD', data['userCardNumber']).encode('ascii','ignore')
    # userExpMonth=unicodedata.normalize('NFKD', data['userExpMonth']).encode('ascii','ignore')
    # userExpYear=unicodedata.normalize('NFKD', data['userExpYear']).encode('ascii','ignore')
    try:
        if session.query(User).filter(User.email == userEmail).first() is  None: 
            new_person =User(name=userName,email=userEmail,unhashpassword=userPassword)
            session.add(new_person)
            session.commit()
    #create and add User Card
            # new_person_card = Card(CardNumber=userCardNumber,expMonth=userExpMonth,expYear=userExpYear,user=new_person)
    
            # session.add(new_person_card)
            # session.commit()
            return jsonify(
            success = True,
            data = {
            'msg': 'Success!! created User!',
             }
            )        
        else:
            return Response(json.dumps("User email is taken!"))
            
    except IntegrityError, e:
        session.rollback()
        return Response(e)
    except InvalidRequestError, e:
        session.rollback()
        return Response(e)
        
@app.route('/follow',methods=['POST'])
def follow_user():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    userFollowedEmail =unicodedata.normalize('NFKD', data['userFollowedEmail']).encode('ascii','ignore')
    new_session= s()
    currentUser_obj = get_user_by_email(currentUserEmail,new_session)
    userFollowed_obj = get_user_by_email(userFollowedEmail,new_session)

    if currentUser_obj.is_following(userFollowed_obj) is not True:
        u = currentUser_obj.follow(userFollowed_obj)
        new_session.add(u)
        new_session.commit()
        response = "Now Following" +" "+ userFollowed_obj.name
        return jsonify(success=True, data=response);
    else:
        response = "This user is already being followed"
        return Response(json.dumps(response))


    
@app.route('/get_followers',methods=['POST'])
def get_followers():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    new_session =s()
    currentUser_obj = get_user_by_email(currentUserEmail,new_session)
    followers = currentUser_obj.get_followers(new_session)
    
    return jsonify(success=True,data=followers)

    

@app.route('/add_post',methods =['POST'])
def add_post():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    post = unicodedata.normalize('NFKD', data['myPost']).encode('ascii','ignore')
    dueIn = unicodedata.normalize('NFKD', data['dueDate']).encode('ascii','ignore')
    start=  unicodedata.normalize('NFKD', data['startTime']).encode('ascii','ignore')
    startTime = datetime.strptime(start,"%Y-%m-%dT%H:%M:%S +0000")
    utcnow = datetime.now()
    add_post_session = s()
    currentUser_obj = get_user_by_email(currentUserEmail,add_post_session)
    p1 = Post(myPost=post, author=currentUser_obj, timestamp=utcnow,dueDate=dueIn,startTime=startTime)
    add_post_session.add(p1)
    add_post_session.commit()
    return Response(json.dumps("Ok"))

   
@app.route('/get_followed_post',methods =['POST'])
def get_followed_post():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    get_post_session = s()
    currentUser_obj = get_user_by_email(currentUserEmail,get_post_session)
    posts = currentUser_obj.followed_posts(get_post_session)
    response = []
    for post in posts:
        post.postedTime =  pretty_date(post.timestamp)
        del post.__dict__['_sa_instance_state']
        del post.__dict__['timestamp']
        response.append(post.__dict__)
    return jsonify(success=True, data=response)
    
@app.route('/get_myposts',methods = ['POST'])
def get_mypost():
    data = request.get_json(force=True)
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    get_mypost_session = s()
    currentUser_obj = get_user_by_email(currentUserEmail,get_mypost_session)
    posts = currentUser_obj.get_myposts(get_mypost_session)
    response = []
    for post in posts:
        post.postedTime =  pretty_date(post.timestamp)
        del post.__dict__['_sa_instance_state']
        del post.__dict__['timestamp']
        response.append(post.__dict__)
    print response
    return jsonify(success=True, data=response)
    
    
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
        like_post_session=s()
        currentUser_obj = get_user_by_email(currentUserEmail,like_post_session)
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