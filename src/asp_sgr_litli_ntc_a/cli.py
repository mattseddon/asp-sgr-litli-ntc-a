import argparse
from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt
from rich.spinner import Spinner

from asp_sgr_litli_ntc_a.config import load_config, write_config
from asp_sgr_litli_ntc_a.linked_in import send_post
from asp_sgr_litli_ntc_a.llm import generate_agent, generate_company, generate_post

DEFAULTS = {
    "agent_name": "Marcus Kent",
    "company_name": "NextUsCRM",
    "company_details": "A CRM company",
}


def _gen_agent(console: Console):
    print("In order to generate a new agent we need to ask a few questions...")

    existing_token = load_config().get("access_token")

    skip = Prompt.ask(
        "Would you like to use the provided defaults?",
        show_choices=True,
        choices=["y", "n"],
    )
    if skip == "y":
        config = DEFAULTS

    else:
        agent_name = Prompt.ask(
            "1. What name would you like to give the agent?",
            show_default=True,
            default=DEFAULTS["agent_name"],
        )
        agent_details = Prompt.ask(
            "2. Any additional information about the agent?",
            show_default=True,
            default="No",
        )
        company_name = Prompt.ask(
            "3. What name would you like to give the agent's company",
            show_default=True,
            default=DEFAULTS["company_name"],
        )
        company_details = Prompt.ask(
            '4. Give a brief description of the SaaS startup company your agent "runs": ',
            show_default=True,
            default=DEFAULTS["company_details"],
        )

        config = {
            "agent_name": agent_name,
            "company_name": company_name,
            "company_details": company_details,
        }

        if agent_details and agent_details != "No":
            config["agent_details"] = agent_details

    if existing_token:
        config["access_token"] = existing_token

    with Live(
        Spinner("dots", text="Generating company"),
        console=console,
        refresh_per_second=10,
    ):
        company_text = generate_company(
            agent_name=config["agent_name"],
            company_name=config["company_name"],
            company_details=config["company_details"],
        )

    config["company"] = company_text

    with Live(
        Spinner("dots", text="Generating agent"), console=console, refresh_per_second=10
    ):
        ceo_text = generate_agent(
            agent_name=config["agent_name"],
            agent_details=config.get("agent_details"),
            company_name=config["company_name"],
            company_text=company_text,
        )

    config["ceo"] = ceo_text

    write_config(config)


def _post(synopsis: str, console: Console):
    config = load_config()

    with Live(
        Spinner("dots", text="Generating post"), console=console, refresh_per_second=10
    ):
        post = generate_post(
            company=config["company"],
            ceo=config["ceo"],
            agent_name=config["agent_name"],
            synopsis=synopsis,
        )

    with Live(
        Spinner("dots", text="Posting to LinkedIn"),
        console=console,
        refresh_per_second=10,
    ):
        send_post(access_token=config["access_token"], text=post)


def _set_token(token: str):
    config = load_config()
    config["access_token"] = token
    write_config(config)


def main():
    parser = argparse.ArgumentParser(
        description="AI slop pushing, sigma grindset riding, LinkedIn thought leader influencer, non-technical CEO agent."
    )
    parser.add_argument(
        "--gen", action="store_true", default=False, help="Generate a new agent."
    )
    parser.add_argument(
        "--post",
        help="Provide a synopsis of a post to generate a new LinkedIn post using your agent.",
    )
    parser.add_argument(
        "--set-token",
        help="Provide your agent with a LinkedIn access token. The agent needs this to be able to post directly to LinkedIn.",
    )

    console = Console()

    args = parser.parse_args()

    if args.gen:
        _gen_agent(console)

    if args.set_token:
        _set_token(args.token)

    if args.post:
        _post(args.post, console)
