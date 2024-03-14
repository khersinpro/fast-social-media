from pydantic import BaseModel

class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    pass

class LikeRead(LikeBase):
    id: int
    user_id: int
    post_id: int

    class Config:
        orm_mode = True

class LikeUpdate(LikeBase):
    pass