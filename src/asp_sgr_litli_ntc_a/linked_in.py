"""
Example call to fetch the member profile for the authorized member.

The 3-legged member access token should include the 'r_liteprofile' scope, which
is part of the Sign In With LinkedIn API product.
"""

from linkedin_api.clients.restli.client import RestliClient

ME_RESOURCE = "/userinfo"

POSTS_RESOURCE = "/posts"
API_VERSION = "202408"


def _escape_text(text):
    chars = ["\\", "|", "{", "}", "@", "[", "]", "(", ")", "<", ">", "#", "*", "_", "~"]
    for char in chars:
        text = text.replace(char, "\\" + char)
    return text


def send_post(access_token: str, text: str) -> None:
    restli_client = RestliClient()
    me_response = restli_client.get(
        resource_path=ME_RESOURCE, access_token=access_token
    )

    escaped_text = _escape_text(text)

    restli_client.create(
        resource_path=POSTS_RESOURCE,
        entity={
            "author": f"urn:li:person:{me_response.entity['sub']}",
            "lifecycleState": "PUBLISHED",
            "visibility": "PUBLIC",
            "commentary": escaped_text,
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
        },
        version_string=API_VERSION,
        access_token=access_token,
    )
