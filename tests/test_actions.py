from rich.console import Console

from asp_sgr_litli_ntc_a.cli import post
from asp_sgr_litli_ntc_a.cli.actions import gen
from asp_sgr_litli_ntc_a.defaults import DEFAULTS
from tests.conftest import generate_ollama_response


def test_gen_skip(
    mock_ollama_generate,
    mock_prompt_ask,
    mock_llm_post_reasoning_response,
    mock_write_config,
):
    mock_config = {}
    gen(Console(), mock_config)
    assert mock_prompt_ask.call_count == 1
    assert mock_write_config.call_count == 1
    mock_write_config.assert_called_once_with(
        {
            **DEFAULTS,
            "ceo": mock_llm_post_reasoning_response,
            "company": mock_llm_post_reasoning_response,
        }
    )


def test_gen_no_blat_token(
    mock_ollama_generate,
    mock_prompt_ask,
    mock_llm_post_reasoning_response,
    mock_write_config,
    mock_access_token,
):
    mock_config = {"access_token": mock_access_token}
    gen(Console(), mock_config)
    assert mock_prompt_ask.call_count == 1
    assert mock_write_config.call_count == 1
    mock_write_config.assert_called_once_with(
        {
            **DEFAULTS,
            "access_token": mock_access_token,
            "ceo": mock_llm_post_reasoning_response,
            "company": mock_llm_post_reasoning_response,
        }
    )


def test_gen(
    mock_ollama_generate,
    mock_prompt_ask,
    mock_llm_post_reasoning_response,
    mock_write_config,
    mock_access_token,
):
    expected_config = {
        "agent_name": "Dave",
        "agent_details": "definitely a sociopath",
        "company_name": "Slopfest inc",
        "company_details": "The newest and bestest Adtech company in the VC game",
    }

    mock_prompt_ask.side_effect = ["n", *expected_config.values()]
    mock_config = {
        **DEFAULTS,
        "ceo": "something, something darkside CEO",
        "company": "builds death stars",
    }
    gen(Console(), mock_config)
    assert mock_prompt_ask.call_count == 5
    assert mock_write_config.call_count == 1
    mock_write_config.assert_called_once_with(
        {
            **expected_config,
            "ceo": mock_llm_post_reasoning_response,
            "company": mock_llm_post_reasoning_response,
        }
    )


def test_post(
    mock_ollama_generate,
    mock_restli_client,
    mock_access_token,
    mock_config,
    mock_llm_post_reasoning_response,
    mock_li_entity_sub,
):
    console = Console()
    post(
        "a fun time we had",
        False,
        console,
        mock_config,
    )
    assert mock_ollama_generate.call_count == 1
    assert mock_restli_client.create.call_count == 1
    mock_restli_client.create.assert_called_once_with(
        resource_path="/posts",
        entity={
            "author": f"urn:li:person:{mock_li_entity_sub}",
            "lifecycleState": "PUBLISHED",
            "visibility": "PUBLIC",
            "commentary": mock_llm_post_reasoning_response,
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
        },
        version_string="202408",
        access_token=mock_access_token,
    )


def test_post_retry(
    mock_ollama_generate,
    mock_restli_client,
    mock_config,
):
    mock_ollama_generate.side_effect = [
        generate_ollama_response(
            f"Okay here is a post by {mock_config['agent_name']}..."
        ),
        generate_ollama_response("**Subject: Let's get SLOPPY**"),
        generate_ollama_response("**Title:** SLOPTASTIC"),
    ]
    post(
        "a fun time we had",
        False,
        Console(),
        mock_config,
    )
    assert mock_ollama_generate.call_count == 3
    assert mock_restli_client.create.call_count == 0


def test_post_preview(
    mock_ollama_generate, mock_restli_client, mock_prompt_ask, mock_config
):
    mock_prompt_ask.return_value = "n"
    post(
        "a preview post",
        True,
        Console(),
        mock_config,
    )
    assert mock_ollama_generate.call_count == 1
    assert mock_restli_client.create.call_count == 0


def test_post_preview_no_config(
    mock_ollama_generate,
    mock_prompt_ask,
    mock_restli_client,
    mock_config_no_token,
    mock_load_config,
    mock_write_config,
):
    mock_prompt_ask.return_value = "y"
    mock_load_config.return_value = {**mock_config_no_token}
    post(
        "a preview post which calls gen",
        True,
        Console(),
        {},
    )
    assert mock_write_config.call_count == 1
    assert mock_ollama_generate.call_count == 3
    assert mock_restli_client.create.call_count == 0
