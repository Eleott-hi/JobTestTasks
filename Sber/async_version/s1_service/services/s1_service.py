from datetime import date
import json
import logging
from typing import Dict, List
import httpx
import asyncio

from fastapi import Depends, HTTPException, status
from models.QueueRequest import QueueRequest, RequestStatus
from models.QueueResponse import QueueResponse
from repositories.queue_request_repository import QueryRequestRepository
from repositories.queue_response_repository import QueryResponseRepository
from configs.config import config

logger = logging.getLogger(__name__)


class S1Service:
    def __init__(
        self,
        queue_request_repository: QueryRequestRepository = Depends(),
        queuer_response_repository: QueryResponseRepository = Depends(),
    ):
        self.client_config = dict(
            base_url=config["s2"]["url"],
            timeout=config["s2"]["timeout"],
            auth=(config["s2"]["login"], config["s2"]["password"]),
        )

        self.queue_request_repository = queue_request_repository
        self.queue_response_repository = queuer_response_repository
        self.offset = 0

    async def process_requests(self, backgrounder: int, limit: int):

        async with httpx.AsyncClient(**self.client_config) as client:
            while True:
                offset = self.offset
                self.offset += limit

                requests, has_next = await self.queue_request_repository.all(
                    offset=offset, limit=limit
                )

                if requests:
                    tasks = [self.__fetch(client, r, backgrounder) for r in requests]
                    responses = await asyncio.gather(*tasks)
                    await self.queue_response_repository.create(responses)
                    await self.queue_request_repository.change_status(
                        requests, RequestStatus.PROCESSED
                    )

                if not has_next:
                    break

    async def __fetch(
        self, client: httpx.AsyncClient, request: QueueRequest, backgrounder
    ) -> QueueResponse:

        try:
            response = await client.request(
                method=request.method,
                url=request.uri,
                params=json.loads(request.params) if request.params else None,
                headers=json.loads(request.headers) if request.headers else None,
            )

            return QueueResponse(
                request_id=request.id,
                status_code=response.status_code,
                body=response.text,
                backgrounder=backgrounder,
            )
        except httpx.ConnectError as e:
            logger.error(e)
            return QueueResponse(
                request_id=request.id,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body="Connection Error",
                backgrounder=backgrounder,
            )
        except httpx.TimeoutException as e:
            logger.error(e)
            return QueueResponse(
                request_id=request.id,
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                body="Gateway Timeout",
                backgrounder=backgrounder,
            )
        except Exception as e:
            logger.error(e)
            return QueueResponse(
                request_id=request.id,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body="Internal Server Error",
                backgrounder=backgrounder,
            )
