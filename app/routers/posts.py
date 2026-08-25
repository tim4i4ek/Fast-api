from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )


    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()