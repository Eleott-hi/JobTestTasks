from datetime import date
from typing import Callable, Dict, List
from app.storage.StorageManager import StorageManager

from app.models.WalletData import WalletData, Operation, OperationCategory
from pathlib import Path
from app.utils import parse_str, parse_str_with_default_if_empty


class UpdateOperationMenu():
    def __init__(self, operation: Operation) -> None:
        d = operation.description
        description = f"{d[:50]}..." if len(d) > 50 else d

        self.operation = {
            "id": {
                "data": operation.id,
            },
            "category": {
                "data": None,
                "input_prompt": f"Category (income/outcome, current: {operation.category}): ",
                "key": OperationCategory,
                "default": operation.category,
            },
            "amount": {
                "data": None,
                "input_prompt": f"Amount (current: {operation.amount}): ",
                "key": float,
                "default": operation.amount,
            },
            "description": {
                "data": None,
                "input_prompt": f"Description (current: {description}): ",
                "key": str,
                "default": operation.description,
            },
            "operation_date": {
                "data": None,
                "input_prompt": f"Date (current: {operation.operation_date}): ",
                "key": date.fromisoformat,
                "default": operation.operation_date,
            },
        }

        self.interface: str = """
        Let's update this operation.
        Skip to save current values.

        [R]epit the menu.
        [B]ack. Go back to the previous menu.
        [Q]uit. Exit the application.
"""

    def run(self) -> Operation | None:
        print(self.interface)
        while True:
            if self.__is_parsing_ready():
                return Operation(
                    id=self.operation["id"]["data"],
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
        for _, value in self.operation.items():
            if value["data"] is None:
                print(value["input_prompt"], end="")
                return

    def __handle_input(self, input_data: str) -> Operation | None:
        match input_data:
            case "r":
                print(self.interface)

            case "q":
                quit()

            case _:
                self.__parse(input_data)

    def __parse(self, input_data: str):
        for _, value in self.operation.items():
            if value["data"] is None:
                value["data"] = parse_str_with_default_if_empty(
                    input_data, key=value["key"], default=value["default"]
                )
                return

    def __is_parsing_ready(self) -> Operation:
        for _, value in self.operation.items():
            if value["data"] is None:
                return False

        return True
