from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import uuid

from .base_dao import BaseDAO
from dtos import PlotDTO

class PlotDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(PlotDTO, session)

    async def create_plot(
        self,
        number: str,
        layout_id: uuid.UUID,
        name: str,
        area_in_acres: float,
        center_coordinates: dict,
        perimeter_coordinates: dict,
        is_sold: bool = False,
        is_active: bool = True,
        description: Optional[str] = None,        
    ) -> PlotDTO:
        return await self.create(
            number=number,
            layout_id=layout_id,
            name=name,
            area_in_acres=area_in_acres,
            center_coordinates=center_coordinates,
            perimeter_coordinates=perimeter_coordinates,
            is_sold=is_sold,
            is_active=is_active,
            description=description
        )
    
    async def get_plot_by_id(self, plot_id: uuid.UUID) -> Optional[PlotDTO]:
        return await self.get_by_id(plot_id)
    
    async def get_plots_by_layout_id(self, layout_id: uuid.UUID) -> List[PlotDTO]:
        result = await self.session.execute(
            select(self.model).where(self.model.layout_id == layout_id)
        )
        return result.scalars().all()
    
    async def update_plot(self, plot_id: uuid.UUID, **kwargs) -> Optional[PlotDTO]:
        return await self.update(plot_id, **kwargs)
    
    async def delete_plot(self, plot_id: uuid.UUID) -> Optional[PlotDTO]:
        return await self.delete(plot_id)