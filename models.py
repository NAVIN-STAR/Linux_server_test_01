from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):

    __tablename__='users'

    id=Column(Integer,index=True,primary_key=True)
    username=Column(String,unique=True,index=True,nullable=False)
    email=Column(String,unique=True,index=True,nullable=False)
    hashed_password=Column(String,nullable=False)





class Coffee(Base):

    __tablename__='coffees'

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True,index=True)
    price=Column(Integer, index=True)

