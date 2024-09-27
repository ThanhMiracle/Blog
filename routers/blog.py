from fastapi import APIRouter , Depends , status , HTTPException
import schemas
import models
from database import get_db
from typing import List
from sqlalchemy.orm import Session
from schemas import Blog
from .repository import blog_repo
from oauth import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)
# , current_user: schemas.User = Depends(get_current_user)
@router.get("/" , status_code=200 , response_model= List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    return blog_repo.get_all(db)


@router.post("/" , status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog , db: Session = Depends(get_db)):
    return blog_repo.create(request , db)

@router.get("/{id}" , status_code=200 , response_model= schemas.ShowBlog)
def get_one_blog(id: int , db: Session = Depends(get_db)):
    return blog_repo.find_blog(id , db)

@router.put("/{id}" , status_code=status.HTTP_202_ACCEPTED ,response_model=schemas.ShowBlog)
def update_blog(id, request: Blog , db: Session = Depends(get_db)):
    return blog_repo.update(id , request ,db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_one_blog(id: int  , db:Session = Depends(get_db)):
    return blog_repo.delete(id , db)