from app.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    likes_count = Column(Integer, default=0)

    author = relationship("User", backref="posts")
