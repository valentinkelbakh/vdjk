import uvicorn
from aiogram import Bot, Dispatcher

from app.utils.database import Data, Database

from .utils.config import (BOT_API_TOKEN, DB_API_URL, DB_LOGIN, DB_PASSWORD,
                           WEBHOOK_PORT)

bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher()
db = Database(DB_API_URL, DB_LOGIN, DB_PASSWORD)
data = Data(db)
config = uvicorn.Config("app.web_app:app", host="0.0.0.0", port=WEBHOOK_PORT, log_level="info")
server = uvicorn.Server(config)
WEBHOOK_URL = ""
