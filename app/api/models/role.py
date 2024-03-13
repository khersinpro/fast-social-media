from sqlalchemy import Column, String, Integer, UniqueConstraint
from app.database import Base


class Role(Base):
    __tablename__ = 'role'

    name = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=True)
