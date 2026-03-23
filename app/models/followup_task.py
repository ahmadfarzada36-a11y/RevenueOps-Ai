from sqlalchemy import Column, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from enum import Enum
from app.db.base_class import Base

class FollowUpStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"


class FollowUpTask(Base):
    __tablename__ = "followup_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)

    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=False)

    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    due_date = Column(DateTime, nullable=False)

    status = Column(
        SQLEnum(
            FollowUpStatusEnum,
            name="followup_status_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        default=FollowUpStatusEnum.pending,
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    deal = relationship("Deal")