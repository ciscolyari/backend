from app.core.security import Hashing
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import CreateUser
from app.core.security import create_access_token
from sqlalchemy.exc import IntegrityError

def create(db:Session, request:CreateUser):
    new_user =User(name=request.name, email=request.email, password=Hashing.hash_password(request.password))
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="coflicts: data already exist"
        )
    

    return new_user

def login(email:str,password: str,db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"incorect user name")
    
    if not Hashing.verify_password(user.password,password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    token=create_access_token({"sub":user.email})
    
    return{
        "access_token":token,
        "token_type":"Bearer"
    }
    
def get(id, db: Session):
    user = db.query(User).filter(User.id==id).first()
    if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with the id {id} is not found"
                )
    return user