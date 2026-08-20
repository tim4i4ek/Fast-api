from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    tags=['authentication']
                   )

@router.post('/login')
def login(User_credentials: schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == User_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail= 'invalid credentials'
        )

    if not utils.verify_password(User_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect password'
        )
    return {"token": "example token"}



