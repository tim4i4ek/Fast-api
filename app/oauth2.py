import os
from jose import JWTError, jwt

#Secret key
#Algorithm
#Expiration time

SECRET_KEY = os.getenv('SECRET_KEY_OAUTH2')
ALGORITHMS = ['HS256']
ACCESS_TOKEN_EXPIRE_MINUTES = 120



