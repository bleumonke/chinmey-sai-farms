from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
import uuid

from .base_dao import BaseDAO
from dtos import CustomerDTO

class CustomerDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(CustomerDTO, session)

    async def create_customer(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        middle_name: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None
    ) -> CustomerDTO:
        return await self.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
        )

    async def update_customer(self, customer_id: uuid.UUID, **kwargs) -> Optional[CustomerDTO]:
        return await self.update(customer_id, **kwargs)

    async def delete_customer(self, customer_id: uuid.UUID) -> Optional[CustomerDTO]:
        return await self.delete(customer_id)

    async def list_customers(self, limit: int = 100) -> List[CustomerDTO]:
        return await self.list_all(limit=limit)

    async def get_by_email(self, email: str) -> Optional[CustomerDTO]:
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> Optional[CustomerDTO]:
        result = await self.session.execute(
            select(self.model).where(self.model.phone == phone)
        )
        return result.scalar_one_or_none()
    
    async def get_by_id(self, customer_id: uuid.UUID) -> Optional[CustomerDTO]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == customer_id)
        )
        return result.scalar_one_or_none()
    
    async def check_email_and_phone(self, email: str, phone: str) -> Optional[CustomerDTO]:
        result = await self.session.execute(
            select(self.model).where(
                (self.model.email == email) | (self.model.phone == phone)
            )
        )
        return result.scalar_one_or_none()