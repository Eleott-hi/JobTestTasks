from datetime import date, datetime
from uuid import UUID, uuid4
import uuid
from sqlalchemy import DateTime, Integer, String, Enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as SQLUUID

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )