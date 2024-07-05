from uuid import UUID
from models.BaseModel import BaseModel
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as SQLUUID


class QueueResponse(BaseModel):
    __tablename__ = "queue_responses"

    status_code: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    body: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    request_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("queue_requests.id"),
        nullable=False,
    )
    backgrounder: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
