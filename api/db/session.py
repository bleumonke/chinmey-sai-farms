from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine
from typing import AsyncGenerator

AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None

def init_session_factory(engine: AsyncEngine):
    global AsyncSessionLocal
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if AsyncSessionLocal is None:
        raise RuntimeError("❌ Session factory is not initialized.")
    async with AsyncSessionLocal() as session:
        yield session
