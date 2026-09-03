
from fastapi import FastAPI    
from fastapi import APIRouter,Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from ..core.database import get_db
from app.schemas.notes import CreateNotes,showUser,showNotes
from app.models.user import User
from app.core.security import get_current_user

from passlib.context import CryptContext
from app.services.note import create,get_all,show,destroy,update

from ..core import database
get_db = database.get_db


router = APIRouter(prefix="/Notes",
    tags=['Notes']
    
)

@router.post("/", status_code=status.HTTP_201_CREATED, )
def create_Notes(request: CreateNotes, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return create(request,db)

@router.get("/", response_model=List[showNotes])
def all(db: Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    return get_all(db)


@router.get("/{id}", status_code=200, response_model=showNotes)
def show_Notes(id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
   return show(id, db)

@router.delete ("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy_Notes(id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
   return destroy(id=id,db=db)



@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_Notes(id: int, request: CreateNotes, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
   return update(id,request,db)



