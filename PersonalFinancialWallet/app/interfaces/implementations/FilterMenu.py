from datetime import date
from typing import Callable, Dict, List
from app.storage.StorageManager import StorageManager

from app.models.WalletData import WalletData, Operation, OperationCategory
from pathlib import Path
from app.utils import parse_str, parse_str_with_default_if_empty
from app.core.StateMachine import StateMachine


class FilterMenu:
    def __init__(self) -> None:
        self.filters: list = []
        self.state_machine = StateMachine()

        self.interface: str = """
        1. Add category
        2. Add amount
        3. Add date
        4. Add description
        5. Search

        [R]epeat the menu
        [C]lear filters
        [B]ack. Go back to the previous menu
        [Q]uit. Exit the application
"""

    def run(self) -> Operation | None:
        self.state_machine.run(self.filters)

    def add_category_filter(self) -> None:
        i = input("Enter the category (income/outcome): ")
        self.filters.append(lambda x: x.category == i)
