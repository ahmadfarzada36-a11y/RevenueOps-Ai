from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Enum as SQLEnum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from enum import Enum
from app.db.base_class import Base

class DealStatusEnum(str, Enum):
    New = "New"
    Quoted = "Quoted"
    FollowUp = "Follow-up"
    Won = "Won"
    Lost = "Lost"


class Deal(Base):
    __tablename__ = "deals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True)

    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), nullable=False)

    deal_value = Column(Numeric(12, 2), nullable=False)

    status = Column(
        SQLEnum(
            DealStatusEnum,
            name="deal_status_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        default=DealStatusEnum.New,
        nullable=False,
        index=True
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    last_contact_date = Column(DateTime)
    next_follow_up_date = Column(DateTime, index=True)

    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    notes = Column(String)

    lead = relationship("Lead", back_populates="deals", lazy="joined")
    customer = relationship("Customer", back_populates="deals")
