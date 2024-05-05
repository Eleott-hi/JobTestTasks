from pydantic import BaseModel, Field
from enum import Enum
from typing import List
from datetime import datetime, date
from uuid import UUID, uuid4


class OperationCategory(str, Enum):
    INCOME = "income"
    OUTCOME = "outcome"


class OperationWrite(BaseModel):
    amount: float
    category: OperationCategory
    description: str = ""
    operation_date: date = date.today()



class Operation(OperationWrite):
    id: UUID = uuid4()

    def __str__(self):
        return f"ID:\t\t{self.id}\nCategory:\t{self.category.value}\nAmount:\t\t{self.amount}\nDate:\t\t{self.operation_date}\nDescription:\t{self.description}\n"

class WalletData(BaseModel):
    operations: List[Operation]
