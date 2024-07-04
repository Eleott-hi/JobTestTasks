import logging
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session
from models.QueueResponse import QueueResponse

logger = logging.getLogger(__name__)


class QueryResponseRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
    ):
        self.session = session

    async def create(self, responses: List[QueueResponse]) -> None:
        for response in responses:
            self.session.add(response)

        try:
            await self.session.commit()
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
