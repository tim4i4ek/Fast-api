from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
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


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""" ,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    return {"data": new_post}



@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    return {"post_detail": post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""" ,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    return {"data": updated_post}



