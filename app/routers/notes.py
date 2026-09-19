
from fastapi import FastAPI, UploadFile, File, Form
from fastapi import APIRouter,Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from ..core.database import get_db
from app.schemas.notes import CreateNotes,showUser,showNotes
from app.models.user import User
from app.core.security import get_current_user
from app.services.note import create
from app.models.notes import Notes

from passlib.context import CryptContext
from app.services.note import create,get_all,show,destroy,update
import shutil
import os

from ..core import database
get_db = database.get_db


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(
    prefix="/Notes",
    tags=['Notes']
    
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_notes(request: CreateNotes, db: Session = Depends(get_db), file:UploadFile=File(None), current_user: User = Depends(get_current_user)):
    return create(request=request, db=db, file=file, user_id=current_user.id)



# @router.post("/with-file", status_code=status.HTTP_201_CREATED)
# def create_notes_with_file(
#     title: str = Form(...),
#     body: str = Form(...),
#     file: UploadFile | None = File(None),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     file_path = None

#     if file:
#         file_path = os.path.join( 
#             UPLOAD_DIR,
#             f"{current_user.id}_{file.filename}"
#         )

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#     new_note = Notes(
#         title=title,
#         body=body,
#         attachment=file_path,
#         user_id=current_user.id
#     )

#     db.add(new_note)
#     db.commit()
#     db.refresh(new_note)

#     return new_note
   



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





