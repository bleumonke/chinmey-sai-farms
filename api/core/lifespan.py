from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from db import (
    create_engine_with_retries,
    init_db,
    init_session_factory
)

import logging.config
import yaml
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    with open("logger.yaml", "r") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    logger.info("🔒 App startup.")
    engine = await create_engine_with_retries()
    init_session_factory(engine)
    await init_db(engine)
    yield
    logger.info("🔒 App shutdown.")
