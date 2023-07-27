from os import path
from pathlib import Path

from envparse import env

app_dir: Path = Path(__file__).parent.parent
env_file = app_dir / ".env"
if path.isfile(env_file):
    env.read_envfile(env_file)
BOT_API_TOKEN = env.str("API_TOKEN", default="")
SERVERLESS = env.bool("SERVERLESS", default=False)
WEBHOOK_HOST = env.str("WEBHOOK_HOST", default="")
WEBHOOK_PATH = env.str("WEBHOOKPATH", default="")
WEBAPP_HOST = env.str("WEBAPP_HOST", default="0.0.0.0")
WEBAPP_PORT = env.int("WEBAPP_PORT", default=3000)
