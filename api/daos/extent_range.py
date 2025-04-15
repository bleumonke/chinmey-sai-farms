from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from dtos import ExtentRange as ExtentRangeDTO

class ExtentRange(Base):
    def __init__(self, session: AsyncSession):
        super().__init__(ExtentRangeDTO, session)