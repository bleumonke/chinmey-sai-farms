from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import uuid

from .base_dao import BaseDAO
from dtos import PaymentModeDTO

class PaymentModeDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(PaymentModeDTO, session)

    async def create_payment_mode(self, name: str) -> PaymentModeDTO:
        return await self.create(name=name)

    async def get_payment_mode_by_id(self, payment_mode_id: uuid.UUID) -> Optional[PaymentModeDTO]:
        return await self.get_by_id(payment_mode_id)

    async def get_all_payment_modes(self, limit: int = 100) -> List[PaymentModeDTO]:
        return await self.list_all(limit=limit)
    
    async def update_payment_mode(self, payment_mode_id: uuid.UUID, **kwargs) -> Optional[PaymentModeDTO]:
        return await self.update(payment_mode_id, **kwargs)
    
    async def delete_payment_mode(self, payment_mode_id: uuid.UUID) -> Optional[PaymentModeDTO]:
        return await self.delete(payment_mode_id)