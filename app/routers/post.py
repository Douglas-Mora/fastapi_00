from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..schemas import PostCreate, Post
from ..database import get_db
from .. oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/{id}", response_model=Post)
def get_post(id:int, db:Session=Depends(get_db),current_user:int=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id '{id}' was not found!")
    else:
        return post


@router.get("/", response_model=List[Post])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(get_current_user)):
    posts = db.query(models.Post).all()
    return posts
    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post:PostCreate,db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id,db:Session=Depends(get_db),current_user:int=Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"'id' {id} was not found.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Intented action is not authorized.")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def update_post(id:int, post:PostCreate,db:Session=Depends(get_db),current_user:int=Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"'id' {id} was not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Intented action is not authorized.")
                            
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
        
