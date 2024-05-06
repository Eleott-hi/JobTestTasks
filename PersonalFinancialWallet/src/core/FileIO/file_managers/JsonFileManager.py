import json

from typing import Annotated, Any
from pathlib import Path
from pydantic import BaseModel

from src.core.FileIO.file_managers.IFileManager import IFileManager


class JsonFileManager(IFileManager):
    def load(self, filename: Path, data_type: Annotated[Any, BaseModel]) -> Any:
        if not issubclass(data_type, BaseModel):
            raise TypeError("Only pydantic models are supported")

        with open(filename, "r") as f:
            data = json.load(f)

        wallet_data = data_type.model_validate(data)
        return wallet_data

    def save(self, filename: Path, data_to_store: Annotated[Any, BaseModel]) -> None:
        if not issubclass(type(data_to_store), BaseModel):
            raise TypeError("Only pydantic models are supported")

        with open(filename, "w") as f:
            f.write(data_to_store.model_dump_json(indent=4))
