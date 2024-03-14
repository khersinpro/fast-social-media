from pydantic import BaseModel

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    author_id: int
    post_id: int

    class Config:
        orm_mode = True

class CommentUpdate(CommentBase):
    pass