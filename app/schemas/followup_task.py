from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class FollowUpStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"

class FollowUpTaskBase(BaseModel):
    due_date: datetime
    status: FollowUpStatusEnum = FollowUpStatusEnum.pending

class FollowUpTaskCreate(FollowUpTaskBase):
    deal_id: UUID
    assigned_user_id: UUID

class FollowUpTaskRead(FollowUpTaskBase):
    id: UUID
    tenant_id: UUID
    deal_id: UUID
    assigned_user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True