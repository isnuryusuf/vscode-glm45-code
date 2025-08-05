from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Item(ItemBase):
    id: int
    completed: bool
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True