from fastapi import HTTPException
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



def Hash_pwd(password:str)->str:
    return pwd_context.hash(password)


def Verify_Pwd(plain_pwd:str,hashed_pwd:str)->bool:
    return pwd_context.verify(plain_pwd,hashed_pwd)


def Create_Access_Token(data:dict,expires_delta:Optional[timedelta]=None) -> str:
    to_encode=data.copy()
    expiry= datetime.now(timezone.utc) +(expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expiry})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def Verify_Access_Token(token:str):
    try:
        payload= jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload

    except JWTError:
         raise HTTPException(status_code=401, detail="Invalid or expired token")



