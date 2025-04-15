from typing import Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class Base:
    def __init__(self, model: Type[Any], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id_: Any) -> Optional[Any]:
        return await self.session.get(self.model, id_)

    async def list_all(self, limit: int = 100) -> List[Any]:
        result = await self.session.execute(select(self.model).limit(limit))
        return result.scalars().all()

    async def create(self, **kwargs) -> Any:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, id_: Any, **kwargs) -> Optional[Any]:
        instance = await self.get_by_id(id_)
        if not instance:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(instance, key):
                setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id_: Any) -> Optional[Any]:
        instance = await self.get_by_id(id_)
        if not instance:
            return None
        await self.session.delete(instance)
        await self.session.commit()
        return instance

    async def exists(self, **filters) -> bool:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
