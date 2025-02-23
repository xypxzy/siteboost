from typing import Optional, Dict
from pydantic import BaseModel, EmailStr
from app.schemas.base import IDSchema


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    subscription_tier: str = "free"
    settings: Optional[Dict] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase, IDSchema):
    pass


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password_hash: str
