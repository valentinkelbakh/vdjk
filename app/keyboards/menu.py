import re

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from app.data.callbacks import BaseCallback
from app.data.states import Menu

start_text = ("Вас приветствует бот VDJKate.\n\n"
              "VDJKate - бот, созданный в рамках Хакатона 2023 "
              "от союза немецкой молодежи Казахстана (Verband der Deutschen Jugend Kasachstans).\n"
              "Бот предоставляет информацию о традиционных немецких блюдах"
              " и праздниках, а также о предстоящих проектах VDJK.\n\n"
              "Выберите, что вам интересно:")


def get_back_btn(back_to):
    if back_to == Menu.MAIN:
        return InlineKeyboardButton(text='Назад', callback_data=BaseCallback(option=Menu.MAIN, page=1).pack())
    elif back_to == Menu.RECIPES:
        return InlineKeyboardButton(text='Назад', callback_data=BaseCallback(option=Menu.RECIPES, page=1).pack())
    elif back_to == Menu.HOLIDAYS:
        return InlineKeyboardButton(text='Назад', callback_data=BaseCallback(option=Menu.HOLIDAYS, page=1).pack())


_main_menu = [
    [InlineKeyboardButton(text='Праздники этнических немцев',
                          callback_data=BaseCallback(option=Menu.HOLIDAYS, page=1).pack())],
    [InlineKeyboardButton(text='Традиционные немецкие блюда',
                          callback_data=BaseCallback(option=Menu.RECIPES, page=1).pack())],
    [InlineKeyboardButton(text='Про СНМК',
                          callback_data=BaseCallback(option=Menu.APPLY, page=1).pack())],
    [InlineKeyboardButton(text='Предстоящие проекты',
                          callback_data=BaseCallback(option=Menu.PROJECTS, page=1).pack())]
]
main_menu = InlineKeyboardMarkup(inline_keyboard=_main_menu)

kb_close_btn = InlineKeyboardButton(text='Закрыть',
                                    callback_data=BaseCallback(option=Menu.DELETE, page=1).pack())
