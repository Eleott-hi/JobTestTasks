from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date, datetime
from enum import Enum as PyEnum

class QueueRequest(BaseModel):
    id: UUID
    uri: str
    method: str
    params: Optional[str] = None
    headers: Optional[str] = None

class QueueResponse(BaseModel):
    status_code: int
    request_id: UUID
    body: Optional[str] = None