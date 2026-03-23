import uuid
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, declarative_base, declared_attr
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()

class Base(DeclarativeBase):
    pass

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()