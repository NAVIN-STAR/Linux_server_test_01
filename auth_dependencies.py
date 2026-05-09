
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
from utils import Verify_Access_Token
from jose import JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")







def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = Verify_Access_Token(token)

        user_email: str = payload.get("sub")

        if user_email is None:
            raise credentials_exception
        
        
        
        return {"email":user_email}

    except JWTError:
        raise credentials_exception
        


    