from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    user = relationship("User", backref="likes")
    post = relationship("Post", backref="likes")
