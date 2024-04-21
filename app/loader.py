import asyncio
import logging
import os

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from app.utils.database import Data, Database

from .utils.config import (
    API_LOGIN,
    API_PASSWORD,
    API_URL,
    BOT_TOKEN,
    WEBHOOK_PORT,
    WORKDIR,
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database(API_URL, API_LOGIN, API_PASSWORD)
data = Data(db)
loop = asyncio.new_event_loop()

i18n = I18n(
    path=os.path.join(WORKDIR, "locales"), default_locale="ru", domain="messages"
)
i18n_middleware = SimpleI18nMiddleware(i18n=i18n)
_ = i18n.gettext
__ = i18n.lazy_gettext
stat_logger = logging.getLogger("bot.stat")
stat_logger.setLevel(logging.INFO)

config = uvicorn.Config(
    "app.web_app:app", host="0.0.0.0", port=WEBHOOK_PORT, log_level="info", loop=loop
)
server = uvicorn.Server(config)
WEBHOOK_URL = ""
