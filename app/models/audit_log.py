import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    action = Column(String, nullable=False)

    entity_type = Column(String)

    entity_id = Column(String)

    details = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)