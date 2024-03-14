from app.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    author = relationship("User", backref="comments")
    post = relationship("Post", backref="comments")