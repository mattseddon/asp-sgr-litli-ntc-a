from unittest.mock import MagicMock
import pytest
from types import SimpleNamespace


@pytest.fixture
def mock_ollama_generate(mocker):
    mock_generate = mocker.patch("asp_sgr_litli_ntc_a.llm.generate")
    # Default response structure
    mock_response = SimpleNamespace(
        {
            "response": "<think>I pretend that I am thinking \n</think>\nThen I send you some garbage",
        }
    )

    mock_generate.return_value = mock_response
    yield mock_generate


@pytest.fixture
def mock_li_entity_sub():
    return "a635b8369"


@pytest.fixture
def mock_restli_client(mocker, mock_li_entity_sub):
    mock_instance = MagicMock()
    mock_client_class = mocker.patch("asp_sgr_litli_ntc_a.linked_in.RestliClient")
    mock_client_class.return_value = mock_instance
    mock_instance.get.return_value = SimpleNamespace(
        {"entity": {"sub": mock_li_entity_sub}}
    )
    mock_instance.create.return_value = None
    yield mock_instance
