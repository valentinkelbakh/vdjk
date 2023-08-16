import aiogram
from aiogram import Bot, Dispatcher

from .utils.config import BOT_API_TOKEN

bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher()
