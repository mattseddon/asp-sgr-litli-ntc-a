from rich.console import Console

from asp_sgr_litli_ntc_a.cli import post


def test_post(
    mock_ollama_generate,
    mock_restli_client,
    mock_access_token,
    mock_config,
    mock_llm_response_after_thinking,
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
            "commentary": mock_llm_response_after_thinking,
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
        },
        version_string="202408",
        access_token=mock_access_token,
    )
