from flask import Flask
import sys,os
import stripe
import unicodedata
from flask import Flask,request,json,Response,jsonify
# from parse_rest.connection import register, ParseBatcher
# from parse_rest.datatypes import Object as ParseObject
# from parse_rest.user import Userpytho
from sqlalchemy import create_engine,update
from sqlalchemy.orm import sessionmaker
from tinyErrandsModel import User,Card
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,orm
Base = declarative_base()
app = Flask(__name__)
engine = create_engine('mysql://admingDa8K2f:Xq4CV8_Br5jU@127.6.142.132:3306')

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
    
@app.route('/hello')
def index():
    return "Hello from OpenShift"

 
if __name__ == '__main__':
    app.run()