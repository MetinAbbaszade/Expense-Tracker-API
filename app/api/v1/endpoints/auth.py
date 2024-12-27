from fastapi import APIRouter, status, HTTPException, Depends
from app.api.v1.schemas.auth import userModel, CustomOAuth2Bearer, create_access_token
from app.extensions import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4, UUID
from datetime import datetime
from app.service import facade
from app.models.user import User

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])

@router.post('/signup', response_model=userModel, status_code=status.HTTP_201_CREATED)
async def signup(user: userModel, db: AsyncSession = Depends(get_db)):
    user.id = uuid4()
    user.created_at = datetime.now()
    user.updated_at = datetime.now()

    existing_user = await facade.get_user(user_id=user.id, db=db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists'
        )
    
    new_user = await facade.add_user(user=user, db=db)
    return new_user

@router.post('/login', response_model=str, status_code=status.HTTP_201_CREATED)
async def login(formdata: CustomOAuth2Bearer = Depends(), db: AsyncSession = Depends(get_db)):
    email = formdata.email
    password = formdata.password
    existing_user: User = await facade.get_user_by_email(email=email, db=db)

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid Email'
        )
    
    if not existing_user.verify_password(password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect Password'
        )
    
    payload = {
        "sub": existing_user.id,
        "username": existing_user.username,
        "email": existing_user.email
    }

    access_token = await create_access_token(payload=payload)

    return access_token