from app.persistence.repository import MemoryRepository
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

class Facade:
    def __init__(self):
        self.user_repo = MemoryRepository(User)

    async def get_all_users(self, db: AsyncSession):
        return await self.user_repo.get_all(session=db)
    
    async def get_user(self, user_id, db: AsyncSession):
        return await self.user_repo.get(obj_id=user_id, session=db)
    
    async def add_user(self, user, db: AsyncSession):
        new_user_data = user.dict()
        new_user = User(**new_user_data)
        await self.user_repo.create(obj=user, session=db)

        return new_user
    
    async def get_user_by_email(self, email, db: AsyncSession):
        users: List[User] = await self.user_repo.get_all(session=db)
        
        for user in users:
            if user.email == email:
                return user