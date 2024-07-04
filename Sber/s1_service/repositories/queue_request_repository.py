import logging
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.QueueRequest import QueueRequest, RequestStatus

# from models.QueueResponse import QueueResponse
from database.database import get_session

logger = logging.getLogger(__name__)


class QueryRequestRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
    ):
        self.session = session

    async def all(self, offset: int = 0, limit: int = 100) -> List[QueueRequest]:
        q = select(QueueRequest)
        q = q.where(QueueRequest.status == RequestStatus.NOT_PROCESSED)
        q1 = q.order_by(QueueRequest.id).offset(offset).limit(limit + 1)

        try:
            res = await self.session.execute(q1)
            res = res.scalars().all()
            await self.change_status(res, status=RequestStatus.PENDING)

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return res[:limit], len(res) == limit + 1

    async def change_status(
        self, requests: List[QueueRequest], status: RequestStatus
    ) -> None:
        for r in requests:
            r.status = status
            self.session.add(r)

        try:
            await self.session.commit()

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
