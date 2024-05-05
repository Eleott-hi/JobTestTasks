from src.core.FileIO.FileManager import FileManager
from src.models.Models import WalletData
from src.core.Wallet import Wallet

class Backend:
    def __init__(self):
        self.wallet = Wallet()
        self.file_manager = FileManager()

    def load(self, filename: str):
        data = self.file_manager.load(filename, WalletData)
        self.wallet.data = data

    def save(self, filename: str):
        data = self.wallet.get_data()
        self.file_manager.save(filename, data)