from typing import List, Union
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str
    firstname: str
    lastname: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    # Config class is used to configure the behavior of the Pydantic model.
    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    email: Union[str, None]
    username: Union[str, None]
    firstname: Union[str, None]
    lastname: Union[str, None]
    password: Union[str, None]