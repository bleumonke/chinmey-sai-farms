from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import uuid

from .base_dao import BaseDAO
from dtos import ExtentRangeDTO

class ExtentRangeDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(ExtentRangeDTO, session)

    async def create_extent_range(
        self,
        label: str,
        unit: str,
        min_value: float,
        max_value: float,
        description: Optional[str],
    ) -> ExtentRangeDTO:
        return await self.create(
            label=label,
            unit=unit,
            min_value=min_value,
            max_value=max_value,
            description=description
        )
    
    async def get_extent_range_by_id(self, extent_range_id: uuid.UUID) -> Optional[ExtentRangeDTO]:
        return await self.get_by_id(extent_range_id)
    
    async def list_extent_ranges(self, limit: int = 100) -> List[ExtentRangeDTO]:
        return await self.list_all(limit=limit)
        
    async def update_extent_range(self, extent_range_id: uuid.UUID, **kwargs) -> Optional[ExtentRangeDTO]:
        return await self.update(extent_range_id, **kwargs)
    
    async def delete_extent_range(self, extent_range_id: uuid.UUID) -> Optional[ExtentRangeDTO]:
        return await self.delete(extent_range_id)