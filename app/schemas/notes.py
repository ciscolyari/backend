from pydantic import BaseModel
from app.schemas.user import showUser
from typing import Optional

         
class CreateNotes(BaseModel):
     title: str
     body: str
     
     class Config():
        from_attributes = True
    

class showNotes(BaseModel):
    title: str
    body: str
    user: Optional[showUser]
    
    class Config():
        orm_mode = True    
                