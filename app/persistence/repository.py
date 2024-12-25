from abc import abstractmethod, ABC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID

class IRepository(ABC):
    @abstractmethod
    def get_all(self, db):
        ...

    @abstractmethod
    def get(self, obj_id, db):
        ...

    @abstractmethod
    def create(self, obj, db):
        ...

    @abstractmethod
    def update(self, obj_id, obj, db):
        ...

    @abstractmethod
    def delete(self, obj_id, db):
        ...


class MemoryRepository(IRepository):
    def __init__(self, model):
        self.model = model

    async def get_all(self, session: AsyncSession):
        objects = session.execute(select(self.model))
        return objects.scalars().all()

    async def get(self, obj_id, session: AsyncSession):
        try:
            if isinstance(obj_id, str):
                obj_id = UUID(obj_id)
            else:
                pass
        except:
            raise ValueError('Id not suitable for UUID')
        
        object = session.execute(select(self.model).where(self.model.id == obj_id))
        return object.scalars().first()

    async def create(self, obj, session: AsyncSession):
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    async def update(self, obj_id, obj, session: AsyncSession):
        existing_object = await self.get(obj_id=obj_id, session=session)
        data = obj.dict()

        for key, value in data:
            setattr(existing_object, key, value)
        
        session.commit()
        session.refresh(existing_object)
        return existing_object

    async def delete(self, obj_id, session: AsyncSession):
        existing_object = await self.get(obj_id=obj_id, session=session)
        session.delete(existing_object)
        session.commit()

        return existing_object