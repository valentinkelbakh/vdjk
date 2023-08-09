from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .middlewares import MyLoggingMiddleware
from .utils.config import BOT_API_TOKEN

bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(MyLoggingMiddleware())
dp.middleware.setup(LoggingMiddleware())
