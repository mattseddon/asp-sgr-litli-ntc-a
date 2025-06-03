import os
import json

CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ".config",
)


def write_config(config: dict[str, str]):
    with open(CONFIG_FILE, "w") as file:
        file.write(json.dumps(config, indent=2))


def load_config() -> dict[str, str]:
    try:
        with open(CONFIG_FILE, "r") as file:
            contents = file.read()
            return json.loads(contents)
    except Exception:
        return {}
