import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import exceptions

from app.data import callbacks as cb
from app.data.states import Menu
from app.loader import bot, dp


@dp.callback_query_handler(cb.base_cb.filter(option=Menu.DELETE))
async def delete_message(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        logging.error(e)


@dp.errors_handler()
async def general_error_handler(update: types.Update, exception: Exception):
    match exception:
        case exceptions.MessageNotModified:
            logging.error(f'⭕ Message not modified')
        case _:
            logging.exception(f'⭕Exception {exception} Exception⭕')
            logging.error(f'\nTraceback ends⭕')
            return None
