import json
import pytest
from pathlib import Path
from pydantic import BaseModel
from typing import Annotated, Any
from unittest.mock import mock_open, patch


class MockModel(BaseModel):
    id: int
    name: str


@pytest.fixture
def json_file_manager():
    from src.core.FileIO.file_managers.JsonFileManager import JsonFileManager

    return JsonFileManager()


@pytest.fixture
def mock_data():
    return {"id": 1, "name": "Test"}


@pytest.fixture
def fake_json_file(tmp_path):
    fake_json_file = tmp_path / "test.json"
    fake_json_file.touch()
    return fake_json_file


def test_load(json_file_manager, mock_data, fake_json_file):

    mock_json_data = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        result = json_file_manager.load(fake_json_file, MockModel)
        assert result.id == 1
        assert result.name == "Test"
        assert isinstance(result, MockModel)


def test_save(json_file_manager, mock_data, fake_json_file):
    data = MockModel(**mock_data)

    with patch("builtins.open", mock_open()):
        json_file_manager.save(fake_json_file, data)

    assert True  # should reach this line


def test_save_not_pydantic_model(json_file_manager, mock_data, fake_json_file):

    with pytest.raises(TypeError):
        with patch("builtins.open", mock_open()):
            json_file_manager.save(fake_json_file, mock_data)


def test_save_not_path(json_file_manager, mock_data):
    with pytest.raises(TypeError):
        json_file_manager.save({}, MockModel)


def test_load_not_pydantic_model(json_file_manager, fake_json_file, mock_data):

    with pytest.raises(TypeError):
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            json_file_manager.load(fake_json_file, str)


def test_load_not_path(json_file_manager, mock_data):
    with pytest.raises(TypeError):
        json_file_manager.load({}, MockModel)


def test_load_not_json_data(json_file_manager, mock_data, fake_json_file):

    with pytest.raises(ValueError):
        with patch("builtins.open", mock_open(read_data="not json data")):
            json_file_manager.load(fake_json_file, MockModel)


def test_load_not_valid_basemodel_data(json_file_manager, mock_data, fake_json_file):

    with pytest.raises(ValueError):
        with patch(
            "builtins.open",
            mock_open(read_data=json.dumps({"not_id": 1, "not_name": "Test"})),
        ):
            json_file_manager.load(fake_json_file, MockModel)
