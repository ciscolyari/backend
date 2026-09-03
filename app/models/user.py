


from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,unique=True)
    email = Column(String, unique=True)
    
    password = Column(String)

    notes = relationship("Notes", back_populates="user")