from datetime import date
from uuid import uuid4
import pytest
from src.models.Models import Operation, OperationWrite, WalletData
from src.core.FileIO.FileManager import FileManager
from src.Application import Application
from src.core.Backend import Backend
from src.core.Wallet import Wallet
import src.view.StateGroups.AddOperationStateGroup as AddSG
import src.view.StateGroups.UpdateOperationStateGroup as UpdateSG


@pytest.fixture
def wallet():
    return Wallet()


@pytest.fixture
def file_manager(monkeypatch, operation):

    monkeypatch.setattr(
        FileManager,
        "load",
        lambda *args, **kwargs: WalletData(
            operations=[Operation(id=uuid4(), **operation.model_dump())]
        ),
    )

    monkeypatch.setattr(FileManager, "save", lambda *args, **kwargs: None)

    return FileManager()


@pytest.fixture
def operation():
    return OperationWrite(
        category="income",
        amount=100,
        operation_date="2021-01-01",
        description="Description 1",
    )


@pytest.fixture
def add_operation(wallet, operation):
    wallet.add_operation(operation)


@pytest.fixture
def app(monkeypatch, wallet, file_manager):

    def mock_init(self):
        self._Backend__wallet = wallet
        self._Backend__file_manager = file_manager

    monkeypatch.setattr(Backend, "__init__", mock_init)

    return Application()


def test_add_operations(monkeypatch, app, wallet):
    user_inputs = iter(
        [
            # "add operation 1"
            "2",
            "1",  # income
            "100",
            "2021-01-01",
            "Description 1",
            # "add operation 2"
            "2",
            "2",  # outcome
            "200",
            "",  # today()
            "Description 2",
            "q",
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()

    assert len(wallet.data.operations) == 2

    assert wallet.data.operations[0].category.value == "income"
    assert wallet.data.operations[0].amount == 100
    assert wallet.data.operations[0].operation_date == date.fromisoformat("2021-01-01")
    assert wallet.data.operations[0].description == "Description 1"

    assert wallet.data.operations[1].category.value == "outcome"
    assert wallet.data.operations[1].amount == 200
    assert wallet.data.operations[1].operation_date == date.today()
    assert wallet.data.operations[1].description == "Description 2"


def test_try_add_operation_but_quit_in_the_middle(monkeypatch, app, wallet):
    user_inputs = iter(["2", "1", "100", "2021-01-01", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()

    assert wallet.data.operations == []


def test_add_invalid_category_input(mocker, monkeypatch, app, wallet):
    spy = mocker.spy(AddSG, "parse_category")

    user_inputs = iter(["2", "invalid", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()

    assert wallet.data.operations == []
    assert spy.call_count == 2
    assert spy.spy_return_list[0] == "category"
    assert spy.spy_return_list[1] == "quit"


def test_add_invalid_amount_input(mocker, monkeypatch, app, wallet):
    spy = mocker.spy(AddSG, "parse_amount")

    user_inputs = iter(["2", "1", "invalid", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()

    assert wallet.data.operations == []
    assert spy.call_count == 2
    assert spy.spy_return_list[0] == "amount"
    assert spy.spy_return_list[1] == "quit"


def test_add_invalid_date_input(mocker, monkeypatch, app, wallet):
    spy = mocker.spy(AddSG, "parse_operation_date")

    user_inputs = iter(["2", "1", "100", "invalid", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()

    assert wallet.data.operations == []
    assert spy.call_count == 2
    assert spy.spy_return_list[0] == "date"
    assert spy.spy_return_list[1] == "quit"


def test_update_operation(mocker, monkeypatch, app, wallet, add_operation, operation):
    id = wallet.data.operations[0].id

    user_inputs = iter(["3", f"{id}", "", "1000", "", "", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()

    assert wallet.data.operations[0].category == operation.category
    assert wallet.data.operations[0].amount == 1000
    assert wallet.data.operations[0].operation_date == operation.operation_date
    assert wallet.data.operations[0].description == operation.description


def test_update_operation_invalid_id(
    mocker, monkeypatch, app, wallet, add_operation, operation
):
    spy = mocker.spy(UpdateSG, "check_id")

    user_inputs = iter(["3", f"{uuid4()}", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()

    assert spy.call_count == 1
    assert spy.spy_return_list[0] == "id"


def test_delete_operation(mocker, monkeypatch, app, wallet, add_operation, operation):
    id = wallet.data.operations[0].id

    user_inputs = iter(["4", f"{id}", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()

    assert len(wallet.data.operations) == 0


def test_load(mocker, monkeypatch, app, wallet, operation):
    user_inputs = iter(["5", "", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()

    assert len(wallet.data.operations) == 1


def test_save(mocker, monkeypatch, app, wallet, operation):
    user_inputs = iter(["6", "", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    app.run()
