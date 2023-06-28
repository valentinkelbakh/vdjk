import re

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from app.data import callbacks as cb
from app.data.states import Menu


def get_back_btn(back_from):
    if back_from == Menu.Holidays:
        return InlineKeyboardButton(text='Назад', callback_data=cb.base_cb.new(option=Menu.Main, page=1))

main_menu = InlineKeyboardMarkup()
main_menu.add(InlineKeyboardButton(text='Немецкие праздники', 
                                    callback_data=cb.base_cb.new(option=Menu.Holidays, page=1)))
main_menu.add(InlineKeyboardButton(text='Ближайший праздник', 
                                    callback_data=cb.base_cb.new(option=Menu.Recipes, page=1)))
