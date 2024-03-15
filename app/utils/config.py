from os import path
from pathlib import Path

from envparse import env

WORKDIR: Path = Path(__file__).parent.parent
env_file = WORKDIR / ".env"
if path.isfile(env_file):
    env.read_envfile(env_file)
BOT_TOKEN = env.str("BOT_TOKEN", default="")
API_URL = env.str("API_URL", default='127.0.0.1:8000/')
API_LOGIN = env.str("API_LOGIN")
API_PASSWORD = env.str("API_PASSWORD")
WEBHOOK = env.bool("WEBHOOK", default=False)
WEBHOOK_PASS = env.str("WEBHOOK_PASS", default="")
WEBHOOK_PORT = env.int("WEBHOOK_PORT", default=8080)
