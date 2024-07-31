from fastapi import APIRouter , Depends , status , HTTPException
import schemas
import models
from database import get_db
from typing import List
from sqlalchemy.orm import Session
from schemas import User
from hash import hash

router = APIRouter()


@router.post('/user' , response_model=schemas.ShowCreator , tags=['user'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    existing_email = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An user with this email already exists."
        )
    new_user = models.User(name = request.name, email = request.email, password = hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{id}", response_model=schemas.ShowUser , tags=['user'])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.ID == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} not found. Try searching with email."
        )
    return user

@router.get("/user/email/{email}", response_model=schemas.ShowUser , tags=['user'])
def get_user_by_name_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found."
        )
    return user


@router.put("/user/{id}", response_model=schemas.ShowUser, tags=['user'])
def user_change(id: int, request: User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.ID == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

    existing_name = db.query(models.User).filter(models.User.name == request.name).first()
    if existing_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with name {request.name} already exists")

    existing_email = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email {request.email} already exists")


    # Update user attributes
    user_data = {
        "name": request.name,
        "email": request.email,
        "password": hash.bcrypt(request.password)
    }
    db.query(models.User).filter(models.User.ID == id).update(user_data)

    db.commit()
    db.refresh(user)

    return user

@router.delete('/user/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['user'])
def delete_user(id , db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.ID == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return "user is deleted!"

