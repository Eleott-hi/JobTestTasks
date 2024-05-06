from typing import List
from uuid import UUID
from app.core.FileIO.FileManager import FileManager
from app.models.Models import Operation, OperationWrite, WalletData
from app.core.Wallet import Wallet


class Backend:
    def __init__(self):
        self.__wallet = Wallet()
        self.__file_manager = FileManager()

    def load(self, filename: str):
        data = self.__file_manager.load(filename, WalletData)
        self.__wallet.set_data(data)

    def save(self, filename: str):
        data = self.__wallet.get_data()
        self.__file_manager.save(filename, data)

    def get_wallet(self) -> Wallet:
        return self.__wallet

    def add_operation(self, data: OperationWrite):
        self.__wallet.add_operation(data)

    def delete_operation(self, id: UUID):
        self.__wallet.delete_operation(id)

    def update_operation(self, data: Operation):
        self.__wallet.update_operation(data)

    def get_operations(self, filters: List | None = None) -> List[Operation]:
        return self.__wallet.get_operations(filters)
    
    def get_operation(self, id: UUID) -> Operation:
        return self.__wallet.get_operation(id)
    
    def check_id(self, id: UUID) -> bool:
        return self.__wallet.check_id(id)