from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.security.auth import jwt_authenticator
from app.api.schemas.post import PostCreate, PostRead, PostUpdate
from app.api.models.post import Post
from app.api.models.user import User
from app.depenencies import get_db

router = APIRouter()

# Get all posts
@router.get("/posts", response_model=list[PostRead])
def get_posts(db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user), skip: int = 0, limit: int = 10):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

# Get all user posts
@router.get("/posts/{user_id}", response_model=list[PostRead])
def get_user_posts(user_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    posts = db.query(Post).filter(Post.author_id == user_id).offset(skip).limit(limit).all()
    return posts

# Create a new post
@router.post("/posts", response_model=PostRead, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)):
    new_post = Post(**post.dict(), author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Update a post
@router.put("/posts/{post_id}", response_model=PostRead)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this post")
    for key, value in post_update.dict().items():
        if value:
            setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post

# Delete a post
@router.delete("/posts/{post_id}", response_model=PostRead)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this post")
    db.delete(post)
    db.commit()
    return post