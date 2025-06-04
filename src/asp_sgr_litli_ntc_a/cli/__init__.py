import argparse
from rich.console import Console

from .actions import gen_agent, post, set_token


def main():
    parser = argparse.ArgumentParser(
        description="AI slop pushing, sigma grindset riding, LinkedIn thought leader influencer, non-technical CEO agent."
    )
    parser.add_argument(
        "--gen", action="store_true", default=False, help="Generate a new agent."
    )
    parser.add_argument(
        "--post",
        metavar="SYNOPSIS",
        help="Provide a synopsis of a post to generate a new LinkedIn post using your agent.",
    )
    parser.add_argument(
        "--set-token",
        metavar="TOKEN",
        help="Provide your agent with a LinkedIn access token. The agent needs this to be able to post directly to LinkedIn.",
    )

    console = Console()

    args = parser.parse_args()

    if args.gen:
        gen_agent(console)

    if args.set_token:
        set_token(args.token)

    if args.post:
        post(args.post, console)
