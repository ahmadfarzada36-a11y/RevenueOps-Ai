from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class DealStatusEnum(str, Enum):
    New = "New"
    Quoted = "Quoted"
    FollowUp = "Follow-up"
    Won = "Won"
    Lost = "Lost"

class DealBase(BaseModel):
    deal_value: float
    status: DealStatusEnum = DealStatusEnum.New
    last_contact_date: Optional[datetime] = None
    next_follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None

class DealCreate(DealBase):
    lead_id: UUID
    assigned_user_id: Optional[UUID] = None

class DealRead(DealBase):
    id: UUID
    tenant_id: UUID
    lead_id: UUID
    assigned_user_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        orm_mode = True