[![tests](https://github.com/mattseddon/asp-sgr-litli-ntc-a/actions/workflows/tests.yml/badge.svg)](https://github.com/mattseddon/asp-sgr-litli-ntc-a/actions/workflows/tests.yml)

# asp-sgr-litli-ntc-a

The CLI in this repository (`liia`) can generate new AI agents and post AI-generated slop directly to LinkedIn from your command line.

![Screenshot 2025-06-04 at 7 32 11 pm (1)](https://github.com/user-attachments/assets/3847703a-ea54-47d1-9259-ef281be6560b)


## Background

Have you, like me, been spending too much time on LinkedIn lately?

Are you sick of reading posts about:
 - The impending extinction of all developers?
 - Vibes replacing skills?
 - LLMs-based coding assistants being **ALL** anyone will need to deliver production-ready code at hyper-speed?

After a couple of months of reading about my impending doom, I realized I could beat all these influencers to the punch by replacing **THEM** with AI agents.

Introducing the AI slop pushing, sigma grindset riding, LinkedIn thought leader influencer, non-technical CEO agent or `asp-sgr-litli-ntc-a` for short.

## Example Posts
<img width="463" alt="Screenshot 2025-06-03 at 11 58 43 am" src="https://github.com/user-attachments/assets/f6f7cf08-b325-40fc-95c6-8d354ec3ad28" />

<br/>
<img width="462" alt="Screenshot 2025-06-03 at 11 42 50 am" src="https://github.com/user-attachments/assets/9b85e7da-1c27-4262-a0f5-7ee6e2ee33f2" />
<br/>
<img width="461" alt="Screenshot 2025-06-03 at 12 56 15 pm" src="https://github.com/user-attachments/assets/2c054049-aa7f-4f69-8768-533b7a82c865" />
<br/>
<img width="465" alt="Screenshot 2025-06-03 at 12 25 02 pm" src="https://github.com/user-attachments/assets/27317f17-7850-4498-83cb-54ad9e7e61f1" />

## Usage

- Create a virtual environment and install the CLI (`uv venv .env && source .env/bin/activate && uv pip install "."`).
- Make sure Ollama is installed and running (see https://ollama.com/ for downloads and run `ollama server`).
- This CLI uses `deepseek-r1` so probably best to pull that too (`ollama pull deepseek-r1`).
- Run the CLI to generate a new agent (`liia --gen`).
- Agent details will now be available in the generated `.config` file.
- Create a LinkedIn profile and generate an access_token (see [here](#creating-a-linkedin-account-for-your-agent) for some help).
- Save the access_token into your config using the CLI (`liia --set-token <NEW_TOKEN>`)
- Run the CLI to generate LinkedIn posts (`liia --post "why you’ll never get caught apologising for driving your team and company so hard."`)

**Note:** `liia --post <SYNOPSIS> --preview` can be used to generate a preview post without running `liia --gen` and/or `liia --set-token <NEW_TOKEN>`.


#### Creating a LinkedIn account for your agent

- First setup an email account for the agent (e.g. a new gmail account).
- Next, setup the LinkedIn account using that email.
- At this point you can use an LLM to generate your profile picture and any sections that you want to fill out.
- Now create an app for the LinkedIn account (at https://www.linkedin.com/developers/apps).
- Under the "Auth" tab use the `OAuth 2.0 tools` link to generate a new access token.


### Disclaimer

Your agent may be flagged as a bot and the account will be "temporarily blocked" until you can verify that the agent is a real person.
At this point you can either get creative and try to bypass the identify checks... or start again :)
