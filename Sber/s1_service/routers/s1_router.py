import asyncio
import logging
from fastapi import APIRouter, status, Depends, BackgroundTasks
from services.s1_service import S1Service
from configs.config import config

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/process_requests",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
)
async def process_requests(
    background_tasks: BackgroundTasks,
    s1_service: S1Service = Depends(),
) -> None:
    tasks = [
        s1_service.process_requests(i, config["buckets"])
        for i in range(config["threads"])
    ]

    async def run_async():
        await asyncio.gather(*tasks)

    background_tasks.add_task(run_async)
