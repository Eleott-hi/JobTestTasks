import asyncio
import logging
from fastapi import APIRouter, status, Depends, BackgroundTasks, HTTPException
from services.s1_service import S1Service
import configs.logger
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

    async def run_async():
        tasks = [
            s1_service.process_requests(i, config["buckets"])
            for i in range(config["threads"])
        ]

        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            raise e
        finally:
            config["in_progress"] = False

    if config["in_progress"]:
        raise HTTPException(status_code=409, detail="Request is already in processing")

    config["in_progress"] = True
    background_tasks.add_task(run_async)
