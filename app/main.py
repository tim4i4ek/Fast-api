from http.client import HTTPException
from fastapi import FastAPI, Response, status, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from passlib.context import CryptContext
from .database import SessionLocal
from sqlalchemy.orm import Session
from . import models,schemas,utils
import os
from typing import List

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


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int,db = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).update({"published": False})
    return post

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.post("posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost,):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s), 
                   RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@app.put("/posts/{id}",response_model=List[schemas.Post])
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    updated_post = models.Post(title=post.title, content=post.content, published=updated_post.published)
    db.commit()
    db.refresh(updated_post)
    return updated_post


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.CreatePost,):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""" ,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    return updated_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}",response_model=schemas.UserOutput)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")













