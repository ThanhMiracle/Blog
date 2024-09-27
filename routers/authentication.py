from fastapi import APIRouter , Depends , HTTPException , status
import schemas
from sqlalchemy.orm import Session
from database import get_db
import models
from hash import hash
from . import token
from datetime import datetime, timedelta, timezone
from schemas import Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



router = APIRouter(
    prefix='/authentication',
    tags=['Authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credential")

    if not hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong password")

    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return Token(access_token=access_token, token_type="bearer")
