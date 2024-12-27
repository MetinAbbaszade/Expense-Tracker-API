from sqlmodel import Field, Column
from app.models.basemodel import BaseModel
from uuid import UUID, uuid4
from decimal import Decimal
from sqlalchemy import String as SAString

class Expense(BaseModel, table=True):
    owner_id: UUID = Field(foreign_key="user.id", nullable=False)
    amount: Decimal = Field(default=0.0, nullable=False)
    category: str = Field(nullable=False)
    description: str | None = Field(default=None)
    payment_method: str | None = Field(default=None)

    def to_dict(self):
        dictionary = super().to_dict()
        dictionary.update({
            'owner_id': str(self.owner_id),
            'amount': float(self.amount),
            'category': self.category,
            'description': self.description,
            'payment_method': self.payment_method,
        })
        return dictionary
