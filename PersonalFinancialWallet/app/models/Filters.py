from pydantic import BaseModel
from enum import Enum
from datetime import date
from app.models.WalletData import OperationCategory


class Composure(str, Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS = "<"
    GREATER = ">"
    LESS_OR_EQUAL = "<="
    GREATER_OR_EQUAL = ">="
    CONTAINS = "contains"


class ComposureForString(str, Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    INCLUDES = "includes"
    NOT_INCLUDES = "not includes"


class DateFilter(BaseModel):
    date: date
    composure: Composure = Composure.EQUAL


class AmountFilter(BaseModel):
    amount: float
    composure: Composure = Composure.EQUAL


class DescriptionFilter(BaseModel):
    description: str
    composure: ComposureForString = ComposureForString.EQUAL


class CategoryFilter(BaseModel):
    category: OperationCategory
