from typing import List, Union
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str
    firstname: str
    lastname: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    # Config class is used to configure the behavior of the Pydantic model.
    class Config:
        orm_mode = True
    