import configs.config
import configs.logger

from fastapi import Depends, FastAPI
from routers.s1_router import router as s1_service_router
from database.database import init_db


async def lifespan(app):
    await init_db()
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="S1 Service",
    description="Service to manage requests queue",
    version="0.0.1",
    root_path="/api/v1",
)


app.include_router(s1_service_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
