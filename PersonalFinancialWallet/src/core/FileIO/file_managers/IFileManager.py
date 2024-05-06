from typing import Annotated, Any
from pathlib import Path
from pydantic import BaseModel


from abc import ABC, abstractmethod


class IFileManager(ABC):

    @abstractmethod
    def load(self, filename: Path, data_type: Annotated[Any, BaseModel]) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def save(self, filename: Path, data: BaseModel):
        raise NotImplementedError()
