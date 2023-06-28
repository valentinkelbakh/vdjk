import re

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from app.data import callbacks as cb
from app.data.states import Menu


def get_back_btn(back_to):
    if back_to == Menu.Main:
        return InlineKeyboardButton(text='Назад', callback_data=cb.base_cb.new(option=Menu.Main, page=1))

main_menu = InlineKeyboardMarkup()
main_menu.add(InlineKeyboardButton(text='Праздники этнических немцев', 
                                    callback_data=cb.base_cb.new(option=Menu.Holidays, page=1)))
main_menu.add(InlineKeyboardButton(text='Традиционные немецкие блюда', 
                                    callback_data=cb.base_cb.new(option=Menu.Recipes, page=1)))
