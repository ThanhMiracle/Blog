from sqlalchemy.orm import Session
import models
from fastapi import HTTPException , status
from schemas import User
import schemas
from hash import hash


def create_user(request: schemas.User, db: Session):
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

def get_user_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.ID == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} not found. Try searching with email."
        )
    return user

def get_user_by_name_email(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found."
        )
    return user


def user_change(id: int, request: User, db: Session):
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

def delete_user(id: int , db:Session):
    user = db.query(models.User).filter(models.User.ID == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return "user is deleted!"