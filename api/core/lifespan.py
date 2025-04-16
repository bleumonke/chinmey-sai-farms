from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from db import (
    setup_database,  # <- replaces create_engine_with_retries + init_db
    init_session_factory
)
import logging.config
import yaml
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()

    # Load logging config
    with open("logger.yaml", "r") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

    logger.info("🔒 App startup.")

    # 💡 Setup database (creates DB, connects, initializes tables)
    engine = await setup_database()
    init_session_factory(engine)

    yield

    logger.info("🔒 App shutdown.")
