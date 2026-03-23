from pydantic import BaseModel
from datetime import datetime


class AIMessageBase(BaseModel):

    lead_id: str
    channel: str
    content: str


class AIMessageCreate(AIMessageBase):
    pass


class AIMessageRead(AIMessageBase):

    id: str
    tenant_id: str
    created_at: datetime

    class Config:
        orm_mode = True