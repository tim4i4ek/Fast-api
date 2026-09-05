from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
    tags=['authentication']
                   )

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail= 'invalid credentials'
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect password'
        )


    access_token = oauth2.create_access_token(data = {"user_id":user.id})

    return {"access_token": access_token}




