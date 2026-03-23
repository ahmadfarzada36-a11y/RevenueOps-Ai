from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRoleEnum(str, Enum):
    admin = "admin"
    sales = "sales"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRoleEnum = UserRoleEnum.sales

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True