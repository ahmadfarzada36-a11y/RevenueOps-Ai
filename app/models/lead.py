from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base_class import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)

    company_name = Column(String, nullable=False)

    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    industry = Column(String)
    source = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="leads")
    deals = relationship("Deal", back_populates="lead")
    converted_to_customer_id = Column(UUID(as_uuid=True), nullable=True)