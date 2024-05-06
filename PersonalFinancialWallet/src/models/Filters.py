from pydantic import BaseModel
from enum import Enum
from datetime import date

from src.models.Models import OperationCategory


class CommonComporator(str, Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="


class DigitalComporator(str, Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS = "<"
    GREATER = ">"
    LESS_OR_EQUAL = "<="
    GREATER_OR_EQUAL = ">="


class StringComporator(str, Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    INCLUDES = "includes"
    NOT_INCLUDES = "excludes"


class DateFilter(BaseModel):
    value: date
    comparator: DigitalComporator

    class Meta:
        compare_field = "operation_date"

    def __str__(self):
        return f"date {self.comparator.value} {self.value}"


class AmountFilter(BaseModel):
    value: float
    comparator: DigitalComporator

    class Meta:
        compare_field = "amount"

    def __str__(self) -> str:
        return f"amount {self.comparator.value} {self.value}"


class DescriptionFilter(BaseModel):
    value: str
    comparator: StringComporator

    class Meta:
        compare_field = "description"

    def __str__(self) -> str:
        return f"description {self.comparator.value} {self.value}"


class CategoryFilter(BaseModel):
    value: OperationCategory
    comparator: CommonComporator

    class Meta:
        compare_field = "category"

    def __str__(self) -> str:
        return f"category {self.comparator.value} {self.value.value}"
