from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class LeadBase(BaseModel):
    company_name: str
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    industry: Optional[str] = None
    source: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadRead(LeadBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True