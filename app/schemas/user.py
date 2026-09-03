from pydantic import BaseModel,EmailStr

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    
class showUser(BaseModel):
    name: str
    email: EmailStr
    class Config():
        orm_mode = True    
        
