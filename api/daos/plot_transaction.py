from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from dtos import PlotTransaction as PlotTransactionDTO

class PlotTransaction(Base):
    def __init__(self, session: AsyncSession):
        super().__init__(PlotTransactionDTO, session)