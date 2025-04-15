from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from dtos import Layout as LayoutDTO

class Layout(Base):
    def __init__(self, session: AsyncSession):
        super().__init__(LayoutDTO, session)