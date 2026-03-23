from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid


class AIMessage(Base):
    __tablename__ = "ai_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, index=True, nullable=False)
    lead_id = Column(String, index=True, nullable=False)

    channel = Column(String)  # email / whatsapp
    content = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())