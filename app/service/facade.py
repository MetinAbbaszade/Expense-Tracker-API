from app.persistence.repository import MemoryRepository
from app.models.user import User
from app.models.expense import Expense
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

class Facade:
    def __init__(self):
        self.user_repo = MemoryRepository(User)
        self.expense_repo = MemoryRepository(Expense)

    async def get_all_users(self, db: AsyncSession):
        return await self.user_repo.get_all(session=db)
    
    async def get_user(self, user_id, db: AsyncSession):
        return await self.user_repo.get(obj_id=user_id, session=db)
    
    async def add_user(self, user, db: AsyncSession):
        new_user_data = user.dict()
        new_user = User(**new_user_data)
        await self.user_repo.create(obj=new_user, session=db)

        return new_user
    
    async def get_user_by_email(self, email, db: AsyncSession):
        users: List[User] = await self.user_repo.get_all(session=db)
        for user in users:
            if user.email == email:
                return user
    
    async def get_all_expenses(self, db: AsyncSession):
        return await self.expense_repo.get_all(session=db)

    async def get_expense(self, expense_id, db: AsyncSession):
        return await self.expense_repo.get(obj_id=expense_id, session=db)

    async def add_expense(self, expense, db: AsyncSession):
        new_expense_data = expense.dict()
        new_expense = Expense(**new_expense_data)
        await self.expense_repo.create(obj=new_expense, session=db)

        return new_expense
    
    async def update_expense(self, expense_id, new_expense, db: AsyncSession):
        new_expense_data = new_expense.dict()
        update_data = Expense(**new_expense_data)
        await self.expense_repo.update(obj_id=expense_id, obj=new_expense, session=db)

        return update_data
    
    async def delete_expense(self, expense_id, db: AsyncSession):
        return await self.expense_repo.delete(obj_id=expense_id, session=db)