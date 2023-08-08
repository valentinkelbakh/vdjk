from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .utils.config import BOT_API_TOKEN

bot = Bot(token=BOT_API_TOKEN)
storage = JSONStorage(r'app/data/storage.json')
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
