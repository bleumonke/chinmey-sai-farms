import os, asyncio, logging
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import text

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
MAX_RETRIES = 5
RETRY_INTERVAL = 3

async def create_engine_with_retries() -> AsyncEngine:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            engine = create_async_engine(DATABASE_URL, echo=False)
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection established.")
            return engine
        except Exception as e:
            logger.warning(f"❌ Database connection failed: {e}")
            if attempt == MAX_RETRIES:
                raise RuntimeError("❌ Could not connect to database.")
            await asyncio.sleep(RETRY_INTERVAL)
