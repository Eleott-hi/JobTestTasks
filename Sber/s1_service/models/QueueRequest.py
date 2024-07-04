from models.BaseModel import BaseModel
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum


class RequestStatus(str, PyEnum):
    NOT_PROCESSED = "not_processed"
    PENDING = "pending"
    PROCESSED = "processed"


class QueueRequest(BaseModel):
    __tablename__ = "queue_requests"

    uri: Mapped[str] = mapped_column(String, nullable=False)
    method: Mapped[str] = mapped_column(String, nullable=False)
    params: Mapped[str] = mapped_column(String, nullable=True)
    headers: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus), nullable=False, default=RequestStatus.NOT_PROCESSED
    )
