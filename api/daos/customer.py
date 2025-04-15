from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from dtos import Customer as CustomerDTO

class Customer(Base):
    def __init__(self, session: AsyncSession):
        super().__init__(CustomerDTO, session)