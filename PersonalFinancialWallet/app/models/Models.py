from pydantic import BaseModel
from enum import Enum
from typing import List
from datetime import date
from uuid import UUID


class OperationCategory(str, Enum):
    INCOME = "income"
    OUTCOME = "outcome"


class OperationWrite(BaseModel):
    amount: float
    category: OperationCategory
    description: str
    operation_date: date


class Operation(OperationWrite):
    id: UUID

    def __str__(self):
        return f"ID:\t\t{self.id}\nCategory:\t{self.category.value}\nAmount:\t\t{self.amount}\nDate:\t\t{self.operation_date}\nDescription:\t{self.description}\n"


class WalletData(BaseModel):
    operations: List[Operation]
