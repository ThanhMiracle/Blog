from sqlalchemy.orm import Session
import models
from fastapi import HTTPException , status
from schemas import Blog

def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: Blog,db: Session):
    existing_title = db.query(models.Blog).filter(models.Blog.title == request.title).first()
    if existing_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A blog with this title already exists. Choose another title."
        )
    new_blog = models.Blog(title=request.title, body=request.body, user_id=2)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def find_blog(id:int ,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.ID == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not available")
    return blog

def delete(id:int , db:Session):
    blog = db.query(models.Blog).filter(models.Blog.ID == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return "blog is deleted!"

def update(id : int ,request: Blog ,  db: Session):
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
    return blog_exist.first()