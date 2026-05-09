from pydantic import BaseModel,EmailStr


class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str # user enters plain password but we hash it before saving into database


class UserRead(BaseModel):
    id:int
    username:str
    email:EmailStr
    
    model_config={
        'from_attributes':True # Enables ORM mode for SQLAlchemy compatibility
    }

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    

class CoffeeCreate(BaseModel):  
    name:str
    price:int


class ReadCoffee(BaseModel):
    id:int
    name:str
    price:int

    model_config={
        'from_attributes':True
    } 

class UpdateCoffee(BaseModel):
    name:str
    price:int



