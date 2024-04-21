from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.data.callbacks import BaseCallback
from app.data.states import Menu
from app.loader import _


def get_back_btn(back_to):
    text = _("Назад")
    if back_to == Menu.MAIN:
        callback_data = BaseCallback(option=Menu.MAIN, page=1)
    elif back_to == Menu.RECIPES:
        callback_data = BaseCallback(option=Menu.RECIPES, page=1)
    elif back_to == Menu.HOLIDAYS:
        callback_data = BaseCallback(option=Menu.HOLIDAYS, page=1)
    return InlineKeyboardButton(text=text, callback_data=callback_data.pack())


def get_main_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                text=_("Праздники этнических немцев"),
                callback_data=BaseCallback(option=Menu.HOLIDAYS, page=1).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=_("Традиционные немецкие блюда"),
                callback_data=BaseCallback(option=Menu.RECIPES, page=1).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=_("Про СНМК"),
                callback_data=BaseCallback(option=Menu.APPLY, page=1).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=_("Предстоящие проекты"),
                callback_data=BaseCallback(option=Menu.PROJECTS, page=1).pack(),
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup


def get_close_btn():
    button = InlineKeyboardButton(
        text=_("Закрыть"), callback_data=BaseCallback(option=Menu.DELETE, page=1).pack()
    )
    return button
