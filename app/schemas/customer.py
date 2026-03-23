from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str
    contact_person: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    industry: str | None = None


class CustomerRead(BaseModel):
    id: UUID
    name: str
    email: str | None

    class Config:
        from_attributes = True