from pathlib import Path

from pydantic import BaseModel

from app.storage.IFileManager import IFileManager
from app.storage.implementations.JsonFileManager import JsonFileManager
from app.models.WalletData import WalletData


class StorageManager:
    def __init__(self):
        self.file_managers = {".json": JsonFileManager[WalletData]()}

    def load(self, filename: str) -> WalletData:
        filename = Path(filename)

        extension = filename.suffix.lower()

        if extension not in self.file_managers:
            raise RuntimeError("File extension not implemented yet: " + extension)

        file_manager = self.file_managers[extension]
        wallet_data: WalletData = file_manager.load(filename, WalletData)
        
        return wallet_data

    def save(self, filename: str, data: BaseModel):
        filename = Path(filename)

        extension = filename.suffix.lower()

        if extension not in self.file_managers:
            raise RuntimeError("File extension not implemented yet: " + extension)

        file_manager = self.file_managers[extension]
        file_manager.save(filename, data)
