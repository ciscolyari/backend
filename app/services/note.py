from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.notes import Notes
from app.schemas.notes import CreateNotes

def get_all(db: Session):
      notes = db.query(Notes).all()
      return notes
    
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
    
    

    