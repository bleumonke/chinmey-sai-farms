from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from .base import Base
from dtos import Crop as CropDTO

class Crop(Base):
    def __init__(self, session: AsyncSession):
        super().__init__(CropDTO, session)
    
    async def get_crop_by_name(self, name: str) -> Optional[CropDTO]:
        stmt = select(CropDTO).where(Crop.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first()