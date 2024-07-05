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
    def __init__(self):
        pass

    async def all(
        self,
        offset: int = 0,
        limit: int = 100,
    ) -> tuple[List[QueueRequest], bool]:
        async with get_session() as session:

            q = (
                select(QueueRequest)
                .order_by(QueueRequest.id)
                .offset(offset)
                .limit(limit + 1)
            )

            try:
                res = await session.execute(q)
                res = res.scalars().all()
                has_next = len(res) == limit + 1
                res = [
                    r for r in res[:limit] if r.status == RequestStatus.NOT_PROCESSED
                ]

                return res, has_next

            except Exception as e:
                logger.error(e)
                raise HTTPException(status_code=500, detail="Internal Server Error")

    async def change_status(self, requests: List[QueueRequest], status: RequestStatus):
        async with get_session() as session:

            q = (
                update(QueueRequest)
                .where(QueueRequest.id.in_([r.id for r in requests]))
                .values(status=status)
            )

            try:
                await session.execute(q)
                await session.commit()

            except Exception as e:
                logger.error(e)
                raise HTTPException(status_code=500, detail="Internal Server Error")
