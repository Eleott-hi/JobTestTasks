import json
from typing import Annotated, Any, override
from pathlib import Path

from pydantic import BaseModel

from app.storage.IFileManager import IFileManager


class JsonFileManager[T](IFileManager[T]):
    @override
    def load(self, filename: Path, data_type: Annotated[Any, BaseModel]) -> Any:
        with open(filename, "r") as f:
            data = json.load(f)

        wallet_data: T = data_type.model_validate(data)
        return wallet_data

    @override
    def save(self, filename: Path, data_to_store: Annotated[Any, BaseModel]) -> None:
        if not issubclass(type(data_to_store), BaseModel):
            raise RuntimeError("Only pydantic models are supported")

        with open(filename, "w") as f:
            f.write(data_to_store.model_dump_json(indent=4))
