from os import path
from pathlib import Path

from envparse import env

app_dir: Path = Path(__file__).parent.parent
env_file = app_dir / ".env"
if path.isfile(env_file):
    env.read_envfile(env_file)
BOT_API_TOKEN = env.str("API_TOKEN", default="")
DB_API_URL = env.str("DB_API_URL", default='127.0.0.1:8000/')
DB_LOGIN = env.str("DB_LOGIN")
DB_PASSWORD = env.str("DB_PASSWORD")
WEBHOOK = env.bool("WEBHOOK", default=False)
WEBHOOK_PASS = env.str("WEBHOOK_PASS", default="")
WEBHOOK_PORT = env.int("WEBHOOK_PORT", default=8080)
