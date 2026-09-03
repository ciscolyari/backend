
from fastapi import FastAPI, APIRouter,Depends, status, HTTPException, Response
from app.services.user import create,get
from app.schemas.user import CreateUser,showUser
from app.models.user import User
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import Hashing
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user import login


router = APIRouter(
    tags=['users'],
    prefix="/user"
)

@router.post('/', response_model=showUser,)
def create_user(request:CreateUser, db: Session = Depends(get_db)):
    return create(db,request)


@router.post('/login')
def loginUser(data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    return login(data.username,data.password,db)


@router.get('/{id}', response_model=showUser,)
def get_user(id: int,db: Session = Depends(get_db)):
   return get(id,db)