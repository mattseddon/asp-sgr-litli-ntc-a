from rich.console import Console

from asp_sgr_litli_ntc_a.cli import post
from tests.conftest import generate_ollama_response


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
        Console(),
        mock_config,
    )
    assert mock_ollama_generate.call_count == 3
    assert mock_restli_client.create.call_count == 0
