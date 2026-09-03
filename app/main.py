from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from app.routers import user, notes
from .core.database import engine,Base


from .routers import user


app=FastAPI()

Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(notes.router)



