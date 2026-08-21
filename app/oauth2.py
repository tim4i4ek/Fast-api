import os
from datetime import datetime, timedelta

from jose import JWTError, jwt

#Secret key
#Algorithm
#Expiration time

SECRET_KEY = os.getenv('SECRET_KEY_OAUTH2')
ALGORITHMS = ['HS256']
ACCESS_TOKEN_EXPIRE_MINUTES = 120


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


