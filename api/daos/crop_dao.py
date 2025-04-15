from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
import uuid

from .base_dao import BaseDAO
from dtos import CropDTO

class CropDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(CropDTO, session)

    async def create_crop(
        self,
        name: str,
    ) -> CropDTO:
        return await self.create(name=name)
    
    async def get_crop_by_id(self, crop_id: uuid.UUID) -> Optional[CropDTO]:
        return await self.get_by_id(crop_id)
    
    async def get_crop_by_name(self, name: str) -> Optional[CropDTO]:
        stmt = select(CropDTO).where(CropDTO.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_all_crops(self) -> List[CropDTO]:
        stmt = select(CropDTO)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def update_layout(self, crop_id: uuid.UUID, **kwargs) -> Optional[CropDTO]:
        return await self.update(crop_id, **kwargs)
    
    async def delete_crop(self, crop_id: uuid.UUID) -> Optional[CropDTO]:
        return await self.delete(crop_id)