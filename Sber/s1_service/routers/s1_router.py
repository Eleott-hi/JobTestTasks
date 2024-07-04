import logging
from fastapi import APIRouter, status, Depends, BackgroundTasks
from services.s1_service import S1Service

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/process_requests",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
)
async def process_requests(
    background_tasks: BackgroundTasks,
    s1_service: S1Service = Depends(),
) -> None:
    # await s1_service.process_requests()
    # for i in range(10):
        background_tasks.add_task(s1_service.process_requests, 0)
