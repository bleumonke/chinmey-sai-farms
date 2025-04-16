from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from dtos import Pricing as PricingDTO

class Pricing(Base):
    def __init__(self, session: AsyncSession):
        super().__init__(PricingDTO, session)