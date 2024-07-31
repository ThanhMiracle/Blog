from fastapi import FastAPI, Depends ,status ,Response , HTTPException
import schemas
from schemas import Blog , User
import models
from database import engine , get_db
from sqlalchemy.orm import Session
from hash import hash
from routers import blog , user

app = FastAPI()
# models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)
app.include_router(blog.router)
app.include_router(user.router)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()












