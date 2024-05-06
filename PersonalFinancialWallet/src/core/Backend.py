from src.core.FileIO.FileManager import FileManager
from src.models.Models import WalletData
from src.core.Wallet import Wallet


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
