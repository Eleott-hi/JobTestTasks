from datetime import date
import pytest
from uuid import uuid4
from src.models.Models import OperationCategory, WalletData, OperationWrite, Operation
from src.models.Filters import (
    CategoryFilter,
    DateFilter,
    AmountFilter,
    DescriptionFilter,
)
from src.core.Comparator import compare
from src.core.Wallet import Wallet

operation1 = OperationWrite(
    category="income",
    amount=100,
    operation_date="2021-01-01",
    description="Description 1",
)

operation2 = OperationWrite(
    category="outcome",
    amount=200,
    operation_date="2022-01-01",
    description="Description 2",
)

operation3 = OperationWrite(
    category="outcome",
    amount=300,
    operation_date="2023-01-01",
    description="Description 3",
)


@pytest.fixture
def wallet():
    return Wallet()


@pytest.fixture
def init_wallet(wallet):
    wallet.add_operation(operation1)
    wallet.add_operation(operation2)
    wallet.add_operation(operation3)


def test_init_wallet(wallet):
    assert wallet.data.operations == []


def test_add_operation(wallet):
    operation_data = OperationWrite(
        category="income",
        amount=100,
        operation_date="2021-01-01",
        description="Description 1",
    )
    wallet.add_operation(operation_data)

    operations = wallet.get_operations()
    data = operations[0]

    assert len(operations) == 1
    assert data.amount == 100
    assert data.category == OperationCategory("income")
    assert data.operation_date == date.fromisoformat("2021-01-01")
    assert data.description == "Description 1"


def test_several_add_operation(wallet, init_wallet):
    operations = wallet.get_operations()
    assert len(operations) == 3

    for original, added in zip(operations, [operation1, operation2, operation3]):
        assert original.amount == added.amount
        assert original.category == added.category
        assert original.operation_date == added.operation_date
        assert original.description == added.description


def test_get_operations_copies_data(wallet, init_wallet):
    operations = wallet.get_operations()
    assert len(operations) == 3

    for added in operations:
        added.amount = 1000

    for added, original in zip(operations, wallet.data.operations):
        assert original.amount != added.amount


def test_get_operations_with_category_filter(wallet, init_wallet):
    filters = [CategoryFilter(comparator="==", value="income")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 1

    filters = [CategoryFilter(comparator="==", value="outcome")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 2

    filters = [CategoryFilter(comparator="!=", value="income")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 2

    filters = [CategoryFilter(comparator="!=", value="outcome")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 1


def test_get_operations_with_date_filter(wallet, init_wallet):
    filters = [DateFilter(comparator="==", value="2020-01-01")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 0

    filters = [DateFilter(comparator="==", value="2021-01-01")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 1
    assert str(operations[0].operation_date) == "2021-01-01"

    filters = [DateFilter(comparator="!=", value="2021-01-01")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 2
    assert str(operations[0].operation_date) == "2022-01-01"
    assert str(operations[1].operation_date) == "2023-01-01"

    filters = [DateFilter(comparator="<", value="2023-01-01")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 2
    assert str(operations[0].operation_date) == "2021-01-01"
    assert str(operations[1].operation_date) == "2022-01-01"

    filters = [DateFilter(comparator="<=", value="2023-01-01")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 3

    filters = [
        DateFilter(comparator="<", value="2023-01-01"),
        DateFilter(comparator=">", value="2021-01-01"),
    ]
    operations = wallet.get_operations(filters)
    assert len(operations) == 1
    assert str(operations[0].operation_date) == "2022-01-01"


def test_get_operations_with_amount_filter(wallet, init_wallet):
    filters = [AmountFilter(comparator="==", value="1000")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 0

    filters = [AmountFilter(comparator="==", value=100)]
    operations = wallet.get_operations(filters)
    assert len(operations) == 1
    assert operations[0].amount == 100

    filters = [AmountFilter(comparator="!=", value=200)]
    operations = wallet.get_operations(filters)
    assert len(operations) == 2
    assert operations[0].amount == 100
    assert operations[1].amount == 300

    filters = [AmountFilter(comparator=">", value=100)]
    operations = wallet.get_operations(filters)
    assert len(operations) == 2
    assert operations[0].amount == 200
    assert operations[1].amount == 300

    filters = [AmountFilter(comparator="<", value=200)]
    operations = wallet.get_operations(filters)
    assert len(operations) == 1
    assert operations[0].amount == 100

    filters = [AmountFilter(comparator=">=", value=200)]
    operations = wallet.get_operations(filters)
    assert len(operations) == 2
    assert operations[0].amount == 200
    assert operations[1].amount == 300

    filters = [
        AmountFilter(comparator="<", value=300),
        AmountFilter(comparator=">", value=100),
    ]
    operations = wallet.get_operations(filters)
    assert len(operations) == 1
    assert operations[0].amount == 200

    filters = [
        AmountFilter(comparator=">=", value=300),
        AmountFilter(comparator="<", value=100),
    ]
    operations = wallet.get_operations(filters)
    assert len(operations) == 0


def test_get_operations_with_description_filter(wallet, init_wallet):
    filters = [DescriptionFilter(comparator="==", value="test")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 0

    filters = [DescriptionFilter(comparator="==", value="Description 1")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 1
    assert operations[0].description == "Description 1"

    filters = [DescriptionFilter(comparator="!=", value="Description 1")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 2
    assert operations[0].description == "Description 2"
    assert operations[1].description == "Description 3"

    filters = [DescriptionFilter(comparator="includes", value="ption")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 3
    assert operations[0].description == "Description 1"
    assert operations[1].description == "Description 2"
    assert operations[2].description == "Description 3"

    filters = [DescriptionFilter(comparator="excludes", value="2")]
    operations = wallet.get_operations(filters)
    assert len(operations) == 2
    assert operations[0].description == "Description 1"
    assert operations[1].description == "Description 3"


def test_get_operations_with_many_types_filter(wallet, init_wallet):
    filters = [
        AmountFilter(comparator="<", value=300),
        CategoryFilter(comparator="==", value="income"),
    ]
    operations = wallet.get_operations(filters)
    assert len(operations) == 1
    assert operations[0].amount == 100
    assert operations[0].category == "income"


def test_get_operation(wallet, init_wallet):
    operations = wallet.get_operations()

    operation_1 = wallet.get_operation(operations[0].id)
    operation_2 = operations[0]

    assert operation_1.id == operation_2.id
    assert operation_1.amount == operation_2.amount
    assert operation_1.category == operation_2.category
    assert operation_1.description == operation_2.description
    assert operation_1.operation_date == operation_2.operation_date


def test_get_operation_copies_data(wallet, init_wallet):
    operations = wallet.get_operations()

    operation_1 = wallet.get_operation(operations[0].id)
    operation_1.amount = 1000

    operations = wallet.get_operations()

    assert operations[0].amount != operation_1


def test_get_operation_not_found(wallet, init_wallet):
    with pytest.raises(ValueError):
        wallet.get_operation(uuid4())


def test_update_operation(wallet, init_wallet):
    operations = wallet.get_operations()
    operation = operations[0]
    operation.amount = 1000
    wallet.update_operation(operation)
    operations = wallet.get_operations()
    assert operations[0].amount == 1000


def test_update_operation_not_found(wallet, init_wallet):
    with pytest.raises(ValueError):
        wallet.update_operation(
            Operation(
                id=uuid4(),
                amount=1000,
                category="income",
                description="test",
                operation_date=date.today(),
            )
        )


def test_delete_operation(wallet, init_wallet):
    operations = wallet.get_operations()
    operation = operations[0]
    wallet.delete_operation(operation.id)

    with pytest.raises(ValueError):
        wallet.get_operation(operation)


def test_delete_operation_not_found(wallet, init_wallet):
    with pytest.raises(ValueError):
        wallet.delete_operation(uuid4())
