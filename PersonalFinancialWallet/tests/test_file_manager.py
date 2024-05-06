from typing import Any
from unittest.mock import patch
import pytest
from pydantic import BaseModel
from src.core.FileIO.IFileManager import IFileManager
from src.core.FileIO.FileManager import FileManager
from pathlib import Path


class MockModel(BaseModel):
    name: str
    age: int


class MockSpecificFileManager(IFileManager):
    def load(self, filename: Path, data_type: BaseModel) -> Any:
        return MockModel(name="test", age=10)

    def save(self, filename: Path, data: BaseModel):
        pass


@pytest.fixture
def mock_data():
    return MockModel(name="test", age=10)


@pytest.fixture
def mock_file_manager(monkeypatch):
    monkeypatch.setattr(
        "src.core.FileIO.FileManager.JsonFileManager",
        MockSpecificFileManager,
    )

    return FileManager()


def test_json_file_load(mock_file_manager, mock_data):
    result = mock_file_manager.load("test.json", MockModel)
    assert result == mock_data


def test_save_data_to_json(mock_file_manager, mock_data):
    with patch.object(MockSpecificFileManager, "save") as mock_save:
        mock_file_manager.save(Path("test.json"), mock_data)

        mock_save.assert_called_once_with(Path("test.json"), mock_data)

def test_load_not_json_file(mock_file_manager):
    with pytest.raises(ValueError):
        mock_file_manager.load("test.txt", MockModel)


def test_save_not_json_file(mock_file_manager, mock_data):
    with pytest.raises(ValueError):
        mock_file_manager.save("test.txt", mock_data)

