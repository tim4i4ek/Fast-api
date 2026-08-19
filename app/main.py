from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from passlib.context import CryptContext
from .database import SessionLocal
import os
from .routers import posts, users
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn = psycopg2.connect(host=os.getenv('HOST').format(),
                                database=os.getenv('DATABASE').format(),
                                user=os.getenv('PASSWORD').format(),
                                password=os.getenv('PASSWORD').format(),
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to PostgreSQL")
        break
    except Exception as error:
        print("Connection failed:", error)
        time.sleep(1)


app.include_router(users.router)
app.include_router(posts.router)














