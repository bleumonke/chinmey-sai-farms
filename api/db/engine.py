import asyncio, logging
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from dtos import Base
from .config import get_db_config

logger = logging.getLogger(__name__)

async def ensure_database_exists():
    config = get_db_config()
    db_name = config["db_name"]
    url_obj = config["url"]
    url_without_db = url_obj.set(database=db_name)
    admin_engine = create_async_engine(url_without_db, echo=False)
    try:
        async with admin_engine.begin() as conn:
            result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"))
            exists = result.scalar()
            if not exists:
                await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                logger.info(f"✅ Database '{db_name}' created.")
            else:
                logger.info(f"✅ Database '{db_name}' already exists.")
    finally:
        await admin_engine.dispose()


async def create_engine_with_retries() -> AsyncEngine:
    await ensure_database_exists()
    config = get_db_config()
    MAX_RETRIES = 5
    RETRY_INTERVAL = 3
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            engine = create_async_engine(config["url"], echo=False)
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection established.")
            return engine
        except OperationalError as e:
            logger.warning(f"❌ Database connection failed (Attempt {attempt}): {e}")
            if attempt == MAX_RETRIES:
                raise RuntimeError("❌ Could not connect to database after retries.")
            await asyncio.sleep(RETRY_INTERVAL)


async def setup_database() -> AsyncEngine:
    engine = await create_engine_with_retries()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Tables created (if not already existing).")
    return engine
