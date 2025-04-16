import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .base import Base
from dtos import Plot as PlotDTO

class Plot(Base):
    def __init__(self, session: AsyncSession):
        super().__init__(PlotDTO, session)
    
    async def get_plots_by_layout_id(self, layout_id: uuid.UUID) -> List[PlotDTO]:
        result = await self.session.execute(
            select(self.model).where(self.model.layout_id == layout_id)
        )
        return result.scalars().all()