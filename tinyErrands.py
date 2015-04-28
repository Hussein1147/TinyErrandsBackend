from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('tinyErrands.cfg')
db = SQLAlchemy(app) 
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key =True)
    name =db.Column(db.String(250),nullable= False)
    email = db.Column(db.String(250))
class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer,primary_key=True)
    CardNumber = db.Column(db.Integer)
    expMonth = db.Column(db.Integer)
    expYear = db.Column(db.Integer)
    cvc = db.Column(db.Integer)
    User_id = db.Column(db.Integer,ForeignKey='user.id')
    user = db.relationship(User)
    
 
@app.route('/')
@app.route('/hello')
def index():
    return "Hello from OpenShift"
 
if __name__ == '__main__':
    app.run()