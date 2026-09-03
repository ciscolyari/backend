from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.models.user import User
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pwdlib import PasswordHash
from app.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

Password_hash=PasswordHash.recommended()
class Hashing:
    @staticmethod
    def hash_password(password: str):
        return Password_hash.hash(password)
    @staticmethod
    def verify_password(hashed_password, plain_password):
        return Password_hash.verify(plain_password, hashed_password)
    


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cfec4333d00c3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")
    return payload
    
        

def get_current_user(token: str = Depends(oauth2_scheme), db:Session=Depends(get_db)):
    payload=verify_token (token)
    email=payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
detail = "Could not validate Credentials",
      headers= {"WWW-authenticate":"Bearer"}  
    )
    user=db.query(User).filter(User.email==email).first()    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" user not found")
    return user
