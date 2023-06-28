import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from app.loader import dp, bot
from app.data.callbacks import base_cb
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

import logging
import requests.exceptions
import urllib3.exceptions
from aiogram.utils import exceptions

from app.data.states import Menu
from app import keyboards as kb


async def update_or_send(message: types.Message,
                         text, keyboard,
                         link=None,
                         parse_mode=None,
                         disable_web_page_preview=None):
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=text,
            reply_markup=keyboard,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview)
    except Exception as e:
        logging.error(e)
        await message.answer(
            text,
            reply_markup=keyboard,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview)
