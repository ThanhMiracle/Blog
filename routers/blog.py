from fastapi import APIRouter , Depends , status , HTTPException
import schemas
import models
from database import get_db
from typing import List
from sqlalchemy.orm import Session
from schemas import Blog

router = APIRouter()

@router.get("/blog" , status_code=200 , response_model= List[schemas.ShowBlog], tags=['blog'])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/blog" , status_code=status.HTTP_201_CREATED , tags=['blog'])
def create_blog(request: Blog , db: Session = Depends(get_db)):
    existing_title = db.query(models.Blog).filter(models.Blog.title == request.title).first()
    if existing_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A blog with this title already exists. Choose another title."
        )
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 2)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blog/{id}" , status_code=200 , response_model= schemas.ShowBlog, tags=['blog'])
def get_one_blog(id: int , db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.ID == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f"blog with id {id} is not available")
    return blog

@router.put("/blog/{id}" , status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(id, request: Blog , db: Session = Depends(get_db)):
    blog_exist = db.query(models.Blog).filter(models.Blog.ID == id)
    if not blog_exist.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")
    existing_title = db.query(models.Blog).filter(models.Blog.title == request.title).first()
    if existing_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A blog with this title already exists."
        )
    blog_data = request.dict()
    blog_exist.update(blog_data)
    db.commit()
    return 'updated'

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def delete_one_blog(id , db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.ID == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return "blog is deleted!"