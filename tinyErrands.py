from flask import Flask
import sys,os
import stripe
import unicodedata
from flask import Flask,request,json,Response,jsonify
from sqlalchemy import create_engine,update
from sqlalchemy.orm import sessionmaker
from tinyErrandsModel import User,Card
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,orm

Base = declarative_base()
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] =True
stripe.api_key = 'sk_test_OM2dp9YnI2w5eNuUKtrxd56g'
engine = create_engine('mysql://admingDa8K2f:Xq4CV8_Br5jU@127.6.142.132:3306/tinyerrands')

s = sessionmaker()
s.configure(bind=engine)
Base.metadata.create_all(engine)
session = s()
@app.route('/')
@app.route('/createUser',methods=['Post'])

def createUser():
    data = request.get_json(force=True)
    userName = unicodedata.normalize('NFKD', data['userName']).encode('ascii','ignore')
    userEmail=unicodedata.normalize('NFKD', data['userEmail']).encode('ascii','ignore')
    userCardNumber=unicodedata.normalize('NFKD', data['userCardNumber']).encode('ascii','ignore')
    userExpMonth=unicodedata.normalize('NFKD', data['userExpMonth']).encode('ascii','ignore')
    userExpYear=unicodedata.normalize('NFKD', data['userExpYear']).encode('ascii','ignore')
    userCvc=unicodedata.normalize('NFKD', data['userCvc']).encode('ascii','ignore')
    
    #create and add User
    new_person =User(name=userName,email=userEmail)
    session.add(new_person)
    session.commit()
    #create and add User Card
    new_person_card = Card(CardNumber=userCardNumber,expMonth=userExpMonth,expYear=userExpYear,cvc=userCvc,user =new_person)
    
    session.add(new_person_card)
    session.commit()
    return Response(json.dumps("Success, Created!"))
    
@app.route('/chargeCard',methods=["POST"])
#here the user card is charged 
def payments_test():
    # register(APPLICATION_ID,REST_API_KEY)
    data = request.get_json(force=True)
    stripeCurrency =unicodedata.normalize('NFKD', data['stripeCurrency']).encode('ascii','ignore')
    stripeAmount =unicodedata.normalize('NFKD', data['stripeAmount']).encode('ascii','ignore')
    stripeDescription=unicodedata.normalize('NFKD', data['stripeDescription']).encode('ascii','ignore')
    currentUserEmail = unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    currentUser_obj = session.query(User).filter(User.email == currentUserEmail).one()
    currentUserCard_obj = session.query(Card).filter(Card.user ==currentUser_obj).one()
    try:
        token = stripe.Token.create(
            card={
                "number":currentUserCard_obj.CardNumber,
                "exp_month":currentUserCard_obj.expMonth,
                "exp_year": currentUserCard_obj.expYear,
                "cvc": currentUserCard_obj.cvc
                },
                )
        charged = stripe.Charge.create(
            description=stripeDescription,
            amount = stripeAmount,
            currency = stripeCurrency,
            source= token.id
            )
        return Response(json.dumps(charged))
    except stripe.error.CardError, e:
        print 'error'
        return Response(json.dumps(e))
    
    
    except stripe.error.InvalidRequestError, e:
        body = e.json_body
        err  = body['error']
        return Response(json.dumps(err))
        
    
@app.route('/transfer', methods=["POST"])

def transfer():
    # register(APPLICATION_ID,REST_API_KEY)
    data = request.get_json(force=True)
    
    currentUserEmail= unicodedata.normalize('NFKD', data['currentUserEmail']).encode('ascii','ignore')
    recipientEmail =unicodedata.normalize('NFKD', data['recipientEmail']).encode('ascii','ignore')
    amount =unicodedata.normalize('NFKD', data['amount']).encode('ascii','ignore')
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
                "cvc": recipientCard_obj.cvc
                },
                )
        
        recipient = stripe.Recipient.create(
            name =recipient_obj.name,
            type ="individual",
            email=recipientEmail,
            card = token.id
            )

        transfer= stripe.Transfer.create(
        amount=amount,
        currency="usd",
        recipient = recipient.id,
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
  

    
    
@app.route('/hello')
def index():
    return "Hello from OpenShift"

 
if __name__ == '__main__':
    app.run()