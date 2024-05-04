from typing import Dict, List
from uuid import UUID

from app.interfaces.implementations.AddOperationMenu import AddOperationMenu
from app.interfaces.implementations.ParserMenu import ParseMenu
from app.interfaces.implementations.UpdateOperationMenu import UpdateOperationMenu
from app.storage.StorageManager import StorageManager
from app.wallet import Wallet
from app.models.WalletData import (
    Operation,
    OperationCategory,
    OperationWrite,
    WalletData,
)


class MainMenu:
    def __init__(self) -> None:
        self.wallet = Wallet()
        self.storage_manager = StorageManager()

        self.title = "Main Menu"

        self.items = {
            **{
                f"{i}": (
                    f"{i}. " + description,
                    callback,
                )
                for i, (description, callback) in enumerate(
                    [
                        ("Load wallet operations from file", self.load),
                        ("Save wallet operations to file", self.save),
                        ("Show wallet data", self.show_wallet),
                        ("Add a new operation", self.add_operation),
                        ("Update an operation", self.update_operation),
                        ("Delete an operation", self.delete_operation),
                    ],
                    start=1,
                )
            },
            None: ("", self.show),
            "r": ("[R]epeat the menu", self.show),
            "q": ("[Q]uit. Exit the application", quit),
        }

    def run(self):
        self.show()

        while True:
            input_data = input(">> ").lower()

            if input_data in self.items:
                self.items[input_data][1]()
            else:
                print("Invalid input. Please try again.")

    def load(self):
        filename: str = input("Enter filename to load data: ")
        try:
            data: WalletData = self.storage_manager.load(filename)
            self.wallet.set_data(data)
            print("Data loaded successfully")
        except Exception as e:
            print("Error loading data: ", e)

    def save(self):
        data: WalletData = self.wallet.get_data()
        filename: str = input("Enter filename to store data: ")
        try:
            self.storage_manager.save(filename, data)
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_operation(self) -> None:
        operation: OperationWrite = AddOperationMenu().run()
        if operation:
            self.wallet.add_operation(operation)
            print(f"Operation added: {operation}")
        else:
            print("Operation not added")

        print(self.interface)

    def show_wallet(self):
        operations = self.wallet.get_operations()

        for operation in operations:
            print("================================================")
            print(operation)

    def update_operation(self):
        id = input("Input operation: ")
        try:
            id = UUID(id)
            operation = self.wallet.get_operation_by_id(id)
            operation = UpdateOperationMenu(operation).run()
            if operation:
                self.wallet.update_operation(operation)
                print(f"Operation updated: {operation}")

        except Exception as e:
            print(f"Error updating operation: {e}")

    def delete_operation(self):
        id = input("Input operation: ")
        try:
            id = UUID(id)
            self.wallet.delete_operation(id)

            print(f"Operation deleted: {id}")

        except Exception as e:
            print(f"Error deleting operation: {e}")

    def show(self):
        print()
        print(self.title)
        print()
        for description, _ in self.items.values():
            print(description)
        print()
