import logging

import aiogram
from aiogram import F, exceptions, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent

from app.data.callbacks import BaseCallback
from app.data.states import Menu
from app.loader import bot, dp


@dp.callback_query(BaseCallback.filter(F.option==Menu.DELETE))
async def delete_message(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        logging.error(e)


@dp.errors()
async def general_error_handler(event: ErrorEvent):
    update = event.update
    exception = event.exception
    match exception:
        case _:
            logging.exception(f'⭕Exception {exception} Exception⭕')
            logging.error(f'\nTraceback ends⭕')
            return None
