from dtos import Base
from sqlalchemy.ext.asyncio import AsyncEngine
from .engine import create_engine_with_retries
from .session import init_session_factory, get_session
import logging

logger = logging.getLogger(__name__)

async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully.")
