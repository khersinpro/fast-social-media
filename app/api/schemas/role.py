from pydantic import BaseModel
from typing import Union

class RoleBase(BaseModel):
    name: str
    description: str

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    class Config:
        orm_mode = True

class RoleUpdate(RoleBase):
    name: Union[str, None]
    description: Union[str, None]