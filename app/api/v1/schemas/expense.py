from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ExpenseModel(BaseModel):
    id: UUID | None = None
    owner_id: UUID | None = None
    amount: int
    category: str
    description: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    payment_method: str