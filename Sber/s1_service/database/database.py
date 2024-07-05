import logging
from typing import AsyncGenerator

import models.QueueRequest, models.QueueResponse
from models.BaseModel import Base
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from configs.config import config


def create_db_url(config) -> Engine:
    db_config = config["database"]

    match db_config.get("dialect", None):
        case "sqlite":
            return f"sqlite+aiosqlite:///{db_config['name']}"
        case "postgresql":
            return f"postgresql+asyncpg://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
        case "mysql":
            return f"mysql+aiomysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
        case _:
            raise ValueError(f"Unsupported database dialect: {db_config['dialect']}")


engine = create_async_engine(create_db_url(config), echo=True, future=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

logger = logging.getLogger(__name__)


async def init_db():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


async def fill_db(cls, data: list):
    async with async_session() as session:
        for d in data:
            session.add(d)
        await session.commit()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:

        logger.info("Session created!")
        yield session
        logger.info("Session closed")
