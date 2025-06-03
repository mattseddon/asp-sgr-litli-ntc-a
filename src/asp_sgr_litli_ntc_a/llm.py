from ollama import generate

CEO_DETAILS = "AI slop pushing, sigma grindset riding, LinkedIn thought leader influencer, non-technical CEO"


def _generate(prompt: str) -> str:
    return generate(
        model="deepseek-r1",
        prompt=prompt,
        stream=False,
    ).response.split("\n</think>\n")[1]


def generate_company(agent_name: str, company_name: str, company_details: str) -> str:
    return _generate(f"""
            Generate a fictitious SaaS startup company.
            The company is named {company_name}.
            The company has an {CEO_DETAILS}.
            The CEO's name is {agent_name}.
            Some additional details about the startup: {company_details}.
            The company should present a positive outlook and masquerade as innovative and profitable but actually have a negative balance sheet and be bleeding cash.
            Marketing spin and perception is far more important to both the CEO and company than the reality of their situation.
            Write about the company as though it is completely real. Start your response with the company's name.
            """)


def generate_agent(
    agent_name: str, agent_details: str | None, company_name: str, company_text: str
) -> str:
    prompt = f"""
            Generate a persona for {agent_name}.
            Here are some details about {agent_name} and the company that he runs {company_name}: {company_text}
            {agent_name} is an {CEO_DETAILS}.
            {agent_name} is completely unhinged in private and sometimes this slips through into your writing.
            {agent_name} looks up to Elon Musk and Mark Zuckerberg as inspirational leaders.
            {agent_name} drives a Tesla and believe that all human workers should be replaced by AI.
            {agent_name} will do anything to cut costs.
            """
    if agent_details:
        prompt = prompt + f"\nSome extra information about {agent_name}: agent_details"

    return _generate(prompt)


def generate_post(company: str, ceo: str, agent_name: str, synopsis: str) -> str:
    return _generate(f"""
        Company details - {company}

        Company's CEO details - {ceo}

        **You are {agent_name}**

        Write a short LinkedIn post detailing {synopsis}.
        Be sure to use standard emojis and the usual bullet point style whilst writing the post.
        Keep it to less than 500 words.
        The returned text must start with the title only and must be ready to be posted to LinkedIn with **NO EDITS** or you go to jail.
        """)
