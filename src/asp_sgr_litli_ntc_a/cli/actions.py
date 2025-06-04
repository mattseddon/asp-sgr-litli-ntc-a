from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt
from rich.spinner import Spinner


from ..config import load_config, write_config
from ..defaults import DEFAULTS
from ..linked_in import send_post
from ..llm import generate_agent, generate_company, generate_post


def gen_agent(console: Console, config=load_config()):
    print("In order to generate a new agent we need to ask a few questions...")

    existing_token = config.get("access_token")

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


def post(synopsis: str, console: Console, config=load_config()):
    if not config:
        print("Cannot generate posts without an agent config")
        print("Please run liia --gen to generate one")

    if not config["access_token"]:
        print("Cannot post to LinkedIn without an access token")
        print("See README for details on how to obtain one")
        return

    waiting_for_post = True
    retries = 0
    while waiting_for_post:
        with Live(
            Spinner("dots", text="Generating post"),
            console=console,
            refresh_per_second=10,
        ):
            agent_name = config["agent_name"]
            text = generate_post(
                company=config["company"],
                ceo=config["ceo"],
                agent_name=agent_name,
                synopsis=synopsis,
            )
            if (
                agent_name in text
                or "subject: " in text.lower()
                or "title: " in text.lower()
            ):
                print("An issue was found with the post text")
                if retries >= 3:
                    print("Maximum number of retries reached")
                    print("Exiting")
                    exit(0)
                retries += 1
                continue
            waiting_for_post = False

    with Live(
        Spinner("dots", text="Posting to LinkedIn"),
        console=console,
        refresh_per_second=10,
    ):
        send_post(access_token=config["access_token"], text=text)


def set_token(token: str, config=load_config()):
    config["access_token"] = token
    write_config(config)
