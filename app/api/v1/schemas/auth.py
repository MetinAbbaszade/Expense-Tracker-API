from pydantic import BaseModel 
from fastapi import Form, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.extensions import get_db
from app.models.user import User
from app.service import facade
import jwt

SECRETKEY = 'superincrediblesuperfantasticsecretmoresecretmostsecretkey'
ALGORITHM = 'HS256'

http_token = HTTPBearer()

class userModel(BaseModel):
    id: UUID | None = None
    username: str 
    email: str
    password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CustomOAuth2Bearer:
    def __init__(
        self,
        email: str = Form(...),
        password: str = Form(...)
    ):
        self.email = email
        self.password = password

async def create_access_token(payload: dict) -> str:
    data = payload.copy()

    for key, value in data.items():
        if isinstance(value, UUID):
            data[key] = str(value)
    
    access_token = jwt.encode(
        payload=data,
        key=SECRETKEY,
        algorithm=ALGORITHM
    )

    return access_token

async def decode_token(token):
    decoded_token = jwt.decode(
        token,
        key=SECRETKEY,
        algorithms=[ALGORITHM]
    )

    return decoded_token


async def generate_token(token: str = Depends(http_token)):
    print(f'This is token which come from httptoken     {token}')
    return token.credentials

async def get_current_user(token: str = Depends(generate_token), db: AsyncSession = Depends(get_db)):
    decoded_token = await decode_token(token=token)
    email: str = decoded_token.get('email')
    user: User = await facade.get_user_by_email(email=email, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    return user