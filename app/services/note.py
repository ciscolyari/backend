from fastapi import status, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.models.notes import Notes
from app.schemas.notes import CreateNotes
import os, shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_CONTENT_TYPES = [
    "applications/PDF",
    "image/JPEG",
    "image/PNG",
    "image/JPG"
]


def get_all(db: Session):
      notes = db.query(Notes).all()
      return notes
    
def create(request: CreateNotes, db: Session, file:UploadFile=None):
    file_path = None
    
    if file:
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail="allowed to upload only PDF or image")
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        
    new_notes = Notes(
        title=request.title,
        body=request.body,
        contentents=request.contentents,
        attachment=file_path,
        user_id=1   
    )
    
    db.add(new_notes)
    db.commit()
    db.refresh(new_notes)
    return new_notes
    
    
    
def create(request:CreateNotes, db: Session):
    new_notes = Notes(title=request.title, body=request.body, user_id=1)
        
    db.add(new_notes)
    db.commit()
    db.refresh(new_notes)
    return new_notes
    
    
def destroy(id: int, db: Session):
    blog = db.query(Notes).filter(Notes.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not found"
        )

    blog.delete(synchronize_session=False)
    db.commit()

    return "done"

def update(id, request:CreateNotes, db: Session):
    blog = db.query(Notes).filter(Notes.id == id)
    if not blog.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blog with the id {id} is not found"
                                )
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'    

def show(id:int, db: Session):
    blog = db.query(Notes).filter(Notes.id == id).first()
    if not blog:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
       
    
       
    return blog
    
    

    