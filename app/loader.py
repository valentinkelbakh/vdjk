import aiogram
from aiogram import Bot, Dispatcher

from .utils.config import BOT_API_TOKEN, DB_API_URL, DB_LOGIN, DB_PASSWORD
from app.utils.database import Database

bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher()
db = Database(DB_API_URL, DB_LOGIN, DB_PASSWORD)
