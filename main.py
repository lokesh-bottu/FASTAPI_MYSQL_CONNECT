from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)



class UserBase(BaseModel):
    username:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


@app.post("/users")
def create_user (user:UserBase,db:db_dependency):

    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}")
def get_users (user_id : int,db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user



# main.py

# from fastapi import FastAPI, HTTPException, Depends, status
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# import models
# from database import engine, SessionLocal

# app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

# class UserBase(BaseModel):
#     username: str

# class UserCreate(UserBase):
#     password: str

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/users")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = models.User(username=user.username, password=user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @app.get("/users/{user_id}")
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     return user
