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

class ContactBase(BaseModel):
    name: str
    email: str
    subject: str
    message: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    created_at: datetime
    is_resolved: bool

    class Config:
        from_attributes = True

class UserAccessBase(BaseModel):
    user_id: int
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    status_code: Optional[int] = None

class UserAccessCreate(UserAccessBase):
    pass

class UserAccess(UserAccessBase):
    id: int
    access_time: datetime
    
    # Include user information
    username: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_contacts: int
    unresolved_contacts: int
    total_items: int
    recent_access_count: int
    access_by_endpoint: dict
    access_by_method: dict
    access_by_status: dict

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