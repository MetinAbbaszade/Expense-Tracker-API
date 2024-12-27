from uuid import UUID, uuid4
from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.extensions import get_db
from typing import List
from app.api.v1.schemas.expense import ExpenseModel
from app.api.v1.schemas.auth import get_current_user
from app.service import facade
from app.models.expense import Expense
from app.models.user import User

router = APIRouter(prefix='/api/v1/expense', tags=['expense'])


@router.get('/', response_model=List[ExpenseModel], status_code=status.HTTP_200_OK)
async def get_all_expenses(
    db: AsyncSession = Depends(get_db)
):
    expenses = await facade.get_all_expenses(db=db)
    if not expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Expenses Not Found'
        )
    data = []
    for expense in expenses:
        data.append(expense.to_dict())
    return data

@router.get('/by-amount', response_model=List[ExpenseModel], status_code=status.HTTP_200_OK)
async def get_expenses_by_amount(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    amount: int = 0
):
    expenses = await facade.get_expenses_by_amount(db=db, owner_id = current_user.id, amount=amount)
    if not expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Expenses Not Found'
        )
    data = []
    for expense in expenses:
        data.append(expense.to_dict())
    return data


@router.get('/{expense_id}', response_model=ExpenseModel, status_code=status.HTTP_200_OK)
async def get_expense(
    expense_id,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):

    expense: Expense = await facade.get_expense(expense_id=expense_id, db=db)

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Expense not found'
        )
    
    if expense.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    
    return expense
    
@router.post('/', response_model=ExpenseModel, status_code=status.HTTP_201_CREATED)
async def add_expense(
    expense: ExpenseModel,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):

    expense.id = uuid4()
    expense.created_at = datetime.now()
    expense.updated_at = datetime.now()

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    expense.owner_id = current_user.id
    new_expense = await facade.add_expense(expense=expense, db=db)

    return new_expense

@router.put('/{expense_id}', response_model=ExpenseModel, status_code=status.HTTP_200_OK)
async def update_expense(
    expense_id, 
    new_expense: ExpenseModel,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):

    expense: Expense = await facade.get_expense(expense_id=expense_id, db=db)

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Expense not found'
        )
    
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    
    if expense.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )

    new_expense.id = expense.id
    new_expense.created_at = expense.created_at
    new_expense.updated_at = datetime.now()
    new_expense.owner_id = expense.owner_id
    updated_expense = await facade.update_expense(expense_id=expense_id, new_expense=new_expense, db=db)

    return updated_expense


@router.delete('/{expense_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):

    expense: Expense = await facade.get_expense(expense_id=expense_id, db=db)

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Expense not found'
        )
    
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    
    if expense.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    
    await facade.delete_expense(expense_id=expense_id, db=db)