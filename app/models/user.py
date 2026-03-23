from sqlalchemy import Column, String, DateTime, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from enum import Enum
from app.db.base_class import Base

class UserRoleEnum(str, Enum):
    admin = "admin"
    sales = "sales"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)

    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    full_name = Column(String)

    role = Column(
        SQLEnum(
            UserRoleEnum,
            name="user_role_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        default=UserRoleEnum.sales,
        nullable=False,
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="users")