from typing import Dict, List
from app.storage.StorageManager import StorageManager

from app.models.WalletData import WalletData
from pathlib import Path


class ParseMenu():
    def __init__(self, data: Dict) -> None:
        self.data = data
        self.storage_manager = StorageManager()

        self.interfaces: str = """
        Let's parse your file!

        [B]ack. Go back to the previous menu.
        [Q]uit. Exit the application.

        Enter path to file: 
"""

    def run(self) -> WalletData:
        print(self.interfaces)
        input_data = input(">>")
        self.__handle_input(input_data)

    def __handle_input(self, filename: str) -> None:
        try:
            self.data["wallet"] = self.storage_manager.parse(filename)
        except Exception as e:
            print(e)
            return
