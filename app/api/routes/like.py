from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.security.auth import jwt_authenticator
from app.api.schemas.like import LikeCreate, LikeRead
from app.api.models.like import Like
from app.api.models.post import Post
from app.api.models.user import User
from app.depenencies import get_db

router = APIRouter()

# Get all post likes
@router.get("/posts/{post_id}", response_model=list[LikeRead])
def get_post_likes(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user), skip: int = 0, limit: int = 10):
    target_post = db.query(Post).filter(Post.id == post_id).first()
    if target_post is None:
        raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
    likes = db.query(Like).filter(Like.post_id == post_id).offset(skip).limit(limit).all()
    return likes

# Create a new like
@router.post("/posts/{post_id}", response_model=LikeRead, status_code=201)
def create_like(post_id: int, like: LikeCreate, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)):
    target_post = db.query(Post).filter(Post.id == post_id).first()
    if target_post is None:
        raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
    already_liked = db.query(Like).filter(Like.user_id == current_user.id, Like.post_id == post_id).first()
    if already_liked:
        target_post.likes_count -= 1
        db.commit()
        raise HTTPException(status_code=400, detail=f'User {current_user.username} already liked post with id {post_id}')
    new_like = Like(**like.dict(), user_id=current_user.id, post_id=post_id)
    target_post.likes_count += 1
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like

# Delete a like
@router.delete("/{like_id}", response_model=LikeRead)
def delete_like(like_id: int, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)):
    like = db.query(Like).filter(Like.id == like_id).first()
    if like is None:
        raise HTTPException(status_code=404, detail="Like not found")
    if like.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this like")
    target_post = db.query(Post).filter(Post.id == like.post_id).first()
    if target_post is None:
        raise HTTPException(status_code=404, detail=f'Post with id {like.post_id} not found')
    target_post.likes_count -= 1
    db.delete(like)
    db.commit()
    return like


