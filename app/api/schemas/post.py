from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    author_id: int
    likes_count: int

    class Config:
        orm_mode = True

class PostUpdate(PostBase):
    pass