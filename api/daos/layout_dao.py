from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import uuid

from .base_dao import BaseDAO
from dtos import LayoutDTO

class LayoutDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(LayoutDTO, session)

    async def create_layout(
        self,
        name: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
        area_in_acres: float,
        center_coordinates: dict,
        perimeter_coordinates: dict,
        description: Optional[str] = None,
    ) -> LayoutDTO:
        return await self.create(
            name=name,
            description=description,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            area_in_acres=area_in_acres,
            center_coordinates=center_coordinates,
            perimeter_coordinates=perimeter_coordinates,
        )

    async def get_layout_by_id(self, layout_id: uuid.UUID) -> Optional[LayoutDTO]:
        return await self.get_by_id(layout_id)

    async def get_all_layouts(self, limit:int = 100) -> List[LayoutDTO]:
        return await self.list_all(limit=limit)
    
    async def update_layout(self, layout_id: uuid.UUID, **kwargs) -> Optional[LayoutDTO]:
        return await self.update(layout_id, **kwargs)
    
    async def delete_layout(self, layout_id: uuid.UUID) -> Optional[LayoutDTO]:
        return await self.delete(layout_id)