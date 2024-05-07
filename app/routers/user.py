from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..schemas import UserCreate,UserResponse
from ..database import get_db
from ..utils import hashing_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    user.password = hashing_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserResponse)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' not found!")
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id)

    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"'id' {id} was not found.")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)