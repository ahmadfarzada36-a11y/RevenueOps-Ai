from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None
    country: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True