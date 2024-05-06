from typing import Annotated, Any, Dict
from pathlib import Path
from pydantic import BaseModel

from app.core.FileIO.file_managers.JsonFileManager import JsonFileManager
from app.core.FileIO.file_managers.IFileManager import IFileManager


class FileManager:
    def __init__(self):
        self.file_managers: Dict[str, IFileManager] = {".json": JsonFileManager()}

    def load(self, filename: str, data_type: Annotated[Any, BaseModel]) -> Any:
        filename = Path(filename)

        extension = filename.suffix
        if extension not in self.file_managers:
            raise ValueError(f'File extension not supported: "{extension}"')

        file_manager = self.file_managers[extension]
        wallet_data = file_manager.load(filename, data_type)

        return wallet_data

    def save(self, filename: str, data: BaseModel):
        filename = Path(filename)

        extension = filename.suffix.lower()

        if extension not in self.file_managers:
            raise ValueError("File extension not implemented yet: " + extension)

        file_manager = self.file_managers[extension]
        file_manager.save(filename, data)
