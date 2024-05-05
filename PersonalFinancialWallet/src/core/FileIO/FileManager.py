
from typing import Annotated, Any
from pathlib import Path
from pydantic import BaseModel

from src.core.FileIO.impl.JsonFileManager import JsonFileManager

class FileManager:
    def __init__(self):
        self.file_managers = {".json": JsonFileManager()}

    def load(self, filename: str, data_type: Annotated[Any, BaseModel]) -> Any:
        filename = Path(filename)

        if not filename.exists():
            raise RuntimeError(f"File not found: {filename}" )

        extension = filename.suffix.lower()
        if extension not in self.file_managers:
            raise RuntimeError(f"File extension not supported: \"{extension}\"" )

        file_manager = self.file_managers[extension]
        wallet_data = file_manager.load(filename, data_type)
        
        return wallet_data

    def save(self, filename: str, data: BaseModel):
        filename = Path(filename)

        extension = filename.suffix.lower()

        if extension not in self.file_managers:
            raise RuntimeError("File extension not implemented yet: " + extension)

        file_manager = self.file_managers[extension]
        file_manager.save(filename, data)
