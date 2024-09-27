from fastapi import APIRouter , Depends , status , HTTPException
import schemas
import models
from database import get_db
from typing import List
from sqlalchemy.orm import Session
from schemas import User
from hash import hash
from .repository import user_repo

router = APIRouter(
    prefix='/user',
    tags= ['User']
)


@router.post('/' , response_model=schemas.ShowCreator)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user_repo.create_user(request , db)

@router.get("/{id}", response_model=schemas.ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_repo.get_user_by_id(id, db)

@router.get("/email/{email}", response_model=schemas.ShowUser)
def get_user_by_name_email(email: str, db: Session = Depends(get_db)):
    return user_repo.get_user_by_name_email(email ,db)


@router.put("/{id}", response_model=schemas.ShowUser)
def user_change(id: int, request: User, db: Session = Depends(get_db)):
    return user_repo.user_change(id , request , db)
    # Update user attributes

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id , db:Session = Depends(get_db)):
    return user_repo.delete_user(id , db)

