from abc import ABC, abstractmethod
from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel


class IFileManager[T](ABC):
    @abstractmethod
    def load(self, file_name: Path, data_type: Annotated[Any, BaseModel]) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def save(self, file_name: Path, data_to_store: T) -> None:
        raise NotImplementedError()
