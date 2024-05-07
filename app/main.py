from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .schemas import Post
from .database import engine, get_db

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


myposts = [{"id":1, "title":"Title for post 1", "content":"Content of post 1"},
           {"id":2, "title":"Favorite food", "content":"That's pizza!"}]


def findpost(id):
    for post in myposts:
        if post["id"] == id:
            return post

def find_post_index(id):
    for i, p in enumerate(myposts):
        if p["id"] == int(id):
            return i


@app.get("/posts/{id}")
def get_post(id:int, db:Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id=%s;""", (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id '{id}' was not found!")
    else:
        return {"message": post}


@app.get("/posts")
def get_posts(db:Session=Depends(get_db)):
    #cursor.execute("""SELECT * from posts;""")
    #posts = cursor.fetchall()
    #return {"data": posts}
    posts = db.query(models.Post).all()
    return {"status":posts}
    

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post,db:Session=Depends(get_db)): #here----
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (post.title, post.content, post.published,))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id,db:Session=Depends(get_db)):
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *; """,(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"'id' {id} was not found.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id:int, post:Post,db:Session=Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *; """, (post.title, post.content,str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"'id' {id} was not found.")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"message":f"Post {id} was updated succesfully!"}
        

