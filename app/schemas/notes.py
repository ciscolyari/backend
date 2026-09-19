from pydantic import BaseModel
from app.schemas.user import showUser
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
         
class CreateNotes(BaseModel):
     title: str
     body: str
    #  file:UploadFile=File(None)
     class Config():
        from_attributes = True
    

class showNotes(BaseModel):
    title: str
    body: str
    #attachment:file_path
    user: Optional[showUser]
    
    class Config():
        orm_mode = True    
                
