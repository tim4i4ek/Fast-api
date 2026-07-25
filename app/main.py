from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.testing import db

from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='tim4i4ek',
                                password='tim4i4ek121209', cursor_factory=RealDictCursor)
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


@app.get("/posts/{id}")
def get_post(id: int,db = Depends(get_db)):
    db.query(models.Post).filter(models.Post.id == id).update({"published": False})


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.post("posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s), 
                   RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""" ,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    db.query(models.Post).filter(models.Post.id == id).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)










