from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.security.auth import jwt_authenticator
from app.api.models.comment import Comment
from app.api.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from app.api.models.post import Post
from app.api.models.user import User
from app.depenencies import get_db

router = APIRouter()

# Get all post comments
@router.get("/posts/{post_id}", response_model=list[CommentRead])
def get_post_comments(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user), skip: int = 0, limit: int = 10):
    comments = db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()
    return comments

# Create a new comment
@router.post("/posts/{post_id}", response_model=CommentRead, status_code=201)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)):
    target_post = db.query(Post).filter(Post.id == post_id).first()
    if target_post is None:
        raise HTTPException(status_code=404, detail=f'Post with id {post_id} not found')
    new_comment = Comment(**comment.dict(), author_id=current_user.id, post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# Update a comment
@router.put("/{comment_id}", response_model=CommentRead)
def update_comment(comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this comment")
    for key, value in comment_update.dict().items():
        if value:
            setattr(comment, key, value)
    db.commit()
    db.refresh(comment)
    return comment

# Delete a comment
@router.delete("/{comment_id}", response_model=CommentRead)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(jwt_authenticator.get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this comment")
    db.delete(comment)
    db.commit()
    return comment
