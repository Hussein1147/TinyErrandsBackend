from flask import Flask
import sys,os
import stripe
import unicodedata
from flask import Flask,request,json,Response,jsonify
# from parse_rest.connection import register, ParseBatcher
# from parse_rest.datatypes import Object as ParseObject
# from parse_rest.user import User
from sqlalchemy import create_engine,update
from sqlalchemy.orm import sessionmaker
from tinyErrandsModel import User,Card
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('tinyErrands.cfg')
db = SQLAlchemy(app) 
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
    db.session.add(new_person)
    db.session.commit()
    #create and add User Card
    new_person_card = Card(CardNumber=userCardNumber,expMonth=userExpMonth,expYear=userExpYear,cvc=userCvc,user =new_person)
    
    db.session.add(new_person_card)
    db.session.commit()
    return Response(json.dumps("Success, Created!"))
    
@app.route('/hello')
def index():
    return "Hello from OpenShift"

 
if __name__ == '__main__':
    app.run()