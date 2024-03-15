import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware
from app.utils.database import Data, Database
import os, logging

from .utils.config import (BOT_TOKEN, API_URL, API_LOGIN, API_PASSWORD,
                           WEBHOOK_PORT, WORKDIR)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database(API_URL, API_LOGIN, API_PASSWORD)
data = Data(db)

i18n = I18n(path=os.path.join(WORKDIR, 'locales'), default_locale="ru", domain="messages")
i18n_middleware = SimpleI18nMiddleware(i18n=i18n)
_ = i18n.gettext
__ = i18n.lazy_gettext
stat_logger = logging.getLogger('bot.stat')
stat_logger.setLevel(logging.INFO)

config = uvicorn.Config("app.web_app:app", host="0.0.0.0", port=WEBHOOK_PORT, log_level="info")
server = uvicorn.Server(config)
WEBHOOK_URL = ""
