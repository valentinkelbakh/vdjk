import asyncio

from app.bot import bot_register
from app.loader import loop, server
from app.utils.config import DB_WEBHOOK

if __name__ == "__main__":
    if DB_WEBHOOK:
        start_app = server.serve
    else:
        start_app = bot_register
    loop.run_until_complete(start_app())
