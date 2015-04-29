from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,ForeignKey,Integer,BigInteger,String
from sqlalchemy.orm import relationship,sessionmaker,mapper
from sqlalchemy import create_engine,orm



Base = declarative_base()
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key =True)
    name =Column(String(250),nullable= False)
    email = Column(String(250))
class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer,primary_key=True)
    CardNumber = Column(BigInteger)
    expMonth = Column(Integer)
    expYear = Column(Integer)
    cvc = Column(Integer)
    User_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)
    
engine = create_engine('mysql://admingDa8K2f:Xq4CV8_Br5jU@127.6.142.132:3306')


Base.metadata.create_all(engine)