import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv('SECRET_KEY_OAUTH2', 'secret_key_for_local_dev')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 120


def create_access_token(data: dict) -> str:

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credentionals_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = str(payload.get("users_id"))

        if id is None:
            raise credentionals_exception
        token_data = schemas.TokenData(id=id)

        return token_data

    except JWTError:
        raise credentionals_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
