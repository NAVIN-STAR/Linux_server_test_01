from fastapi import APIRouter, Depends,HTTPException
import schemas,models
from database import get_db
from sqlalchemy.orm import Session
import utils
from fastapi.security import OAuth2PasswordRequestForm


router=APIRouter()

@router.post("/register/",response_model=schemas.UserRead)
def Register(user:schemas.UserCreate,db:Session=Depends(get_db)):
    
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail={"message":"User with this email already exists"})
    
    hashed_pwd=utils.Hash_pwd(user.password)
  
    
    db_user=models.User(username=user.username,email=user.email,hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
    
@router.post("/login/")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    
    db_user=db.query(models.User).filter(models.User.email==form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found")
    
    if not utils.Verify_Pwd(form_data.password,db_user.hashed_password):
        raise HTTPException(status_code=401,detail="Incorrect password")
    
    access_token=utils.Create_Access_Token(data={"sub":db_user.email})
   
    
    return {"access_token":access_token,"token_type":"bearer"}