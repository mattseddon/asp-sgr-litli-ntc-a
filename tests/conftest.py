from unittest.mock import MagicMock
import pytest
from types import SimpleNamespace

from asp_sgr_litli_ntc_a.defaults import DEFAULTS

LLM_REASONING_TEXT = "<think>I pretend that I am thinking \n</think>\n"


@pytest.fixture
def mock_llm_post_reasoning_response():
    return "Then I send you some garbage"


def generate_ollama_response(text: str) -> SimpleNamespace:
    return SimpleNamespace(response=f"{LLM_REASONING_TEXT}{text}")


@pytest.fixture
def mock_ollama_generate(mocker, mock_llm_post_reasoning_response):
    mock_generate = mocker.patch("asp_sgr_litli_ntc_a.llm.generate")
    mock_response = generate_ollama_response(mock_llm_post_reasoning_response)

    mock_generate.return_value = mock_response
    return mock_generate


@pytest.fixture
def mock_access_token():
    return "not a token"


@pytest.fixture(autouse=True)
def mock_write_config(mocker):
    return mocker.patch("asp_sgr_litli_ntc_a.cli.actions.write_config")


@pytest.fixture
def mock_load_config(mocker):
    return mocker.patch("asp_sgr_litli_ntc_a.cli.actions.load_config")


@pytest.fixture
def mock_config_no_token():
    return {
        **DEFAULTS,
        "company": "AI slop generated company details",
        "ceo": "AI slop generated company details",
    }


@pytest.fixture
def mock_config(mock_config_no_token, mock_access_token):
    return {
        **mock_config_no_token,
        "access_token": mock_access_token,
    }


@pytest.fixture
def mock_li_entity_sub():
    return "a635b8369"


@pytest.fixture
def mock_prompt_ask(mocker):
    mock_prompt_ask = mocker.patch("asp_sgr_litli_ntc_a.cli.actions.Prompt.ask")
    mock_prompt_ask.return_value = "y"
    return mock_prompt_ask


@pytest.fixture
def mock_restli_client(mocker, mock_li_entity_sub):
    mock_instance = MagicMock()
    mock_client_class = mocker.patch("asp_sgr_litli_ntc_a.linked_in.RestliClient")
    mock_client_class.return_value = mock_instance
    mock_instance.get.return_value = SimpleNamespace(entity={"sub": mock_li_entity_sub})
    mock_instance.create.return_value = None
    return mock_instance
