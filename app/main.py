from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from passlib.context import CryptContext #Remove this line
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .schemas import PostBase, PostCreate, PostResponse, UserCreate,UserResponse
from .database import engine, get_db
from .utils import hashing_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #Remove also

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database="fastapi", user="postgres", password="@MspudD7!", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfully connected to database!")
        break
    except Exception as error:
        print("Connection error occurred!")
        print(f"Error: {error}")
        time.sleep(2)


# -------------- POSTS
@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id:int, db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id '{id}' was not found!")
    else:
        return post


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post:PostCreate,db:Session=Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"'id' {id} was not found.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(id:int, post:PostCreate,db:Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"'id' {id} was not found.")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
        

# -------------- USERS
@app.get("/users")
def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    user.password = hashing_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model=UserResponse)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' not found!")
    return user


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id)

    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"'id' {id} was not found.")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)