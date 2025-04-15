from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from dtos import PaymentMode as PaymentModeDTO

class PaymentMode(Base):
    def __init__(self, session: AsyncSession):
        super().__init__(PaymentModeDTO, session)