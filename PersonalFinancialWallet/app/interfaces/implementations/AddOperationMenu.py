from datetime import date
from typing import Callable, Dict, List
from app.storage.StorageManager import StorageManager

from app.models.WalletData import WalletData, OperationWrite, OperationCategory
from pathlib import Path


class AddOperationMenu():
    def __init__(self) -> None:
        self.operation = {
            "category": {
                "data": None,
                "input_prompt": "Category (income/outcome): ",
                "key": OperationCategory,
                "default": None,
            },
            "amount": {
                "data": None,
                "input_prompt": "Amount: ",
                "key": float,
                "default": None,
            },
            "description": {
                "data": None,
                "input_prompt": "Description: ",
                "key": str,
                "default": None,
            },
            "operation_date": {
                "data": None,
                "input_prompt": "Date (e.g. 2021-01-01, default: today): ",
                "key": date.fromisoformat,
                "default": date.today(),
            },
        }

        self.interface: str = """
        Let's add a new operation to the wallet.

        [R]epit the menu.
        [B]ack. Go back to the previous menu.
        [Q]uit. Exit the application.
"""

    def run(self) -> OperationWrite | None:
        print(self.interface)
        while True:
            if self.__is_parsing_ready():
                return OperationWrite(
                    amount=self.operation["amount"]["data"],
                    category=self.operation["category"]["data"],
                    description=self.operation["description"]["data"],
                    operation_date=self.operation["operation_date"]["data"],
                )

            self.__print_data()
            input_data = input()

            if input_data == "b":
                return

            self.__handle_input(input_data)

    def __print_data(self) -> None:
        for key, value in self.operation.items():
            if value["data"] is None:
                print(value["input_prompt"], end="")
                return

    def __handle_input(self, input_data: str) -> OperationWrite | None:
        match input_data:
            case "r":
                print(self.interface)

            case "q":
                quit()

            case _:
                self.__parse(input_data)

    def __parse(self, input_data: str):
        for key, value in self.operation.items():
            if value["data"] is None:
                value["data"] = self.__parse_data(
                    input_data, key=value["key"], default=value["default"]
                )
                return

    def __parse_data(self, data, key: Callable, default=None):
        if default and data == "":
            return default

        try:
            return key(data)
        except ValueError as e:
            print(f"Invalid id input: {data}\nTry again")

    def __is_parsing_ready(self) -> OperationWrite:
        for key, value in self.operation.items():
            if value["data"] is None:
                return False

        return True
