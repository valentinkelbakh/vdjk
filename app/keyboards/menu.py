import re

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from app.data import callbacks as cb
from app.data.states import Menu

start_text = ("Привет, {}\n"
              "Вас приветствует бот VDJKate.\n"
              "Вы можете ознакомиться с моим функционалом, перейдя по ссылкам снизу!")


def get_back_btn(back_to):
    if back_to == Menu.MAIN:
        return InlineKeyboardButton(text='Назад', callback_data=cb.base_cb.new(option=Menu.MAIN, page=1))
    elif back_to == Menu.RECIPES:
        return InlineKeyboardButton(text='Назад', callback_data=cb.base_cb.new(option=Menu.RECIPES, page=1))
    elif back_to == Menu.HOLIDAYS:
        return InlineKeyboardButton(text='Назад', callback_data=cb.base_cb.new(option=Menu.HOLIDAYS, page=1))


main_menu = InlineKeyboardMarkup()
main_menu.add(InlineKeyboardButton(text='Праздники этнических немцев',
                                   callback_data=cb.base_cb.new(option=Menu.HOLIDAYS, page=1)))
main_menu.add(InlineKeyboardButton(text='Традиционные немецкие блюда',
                                   callback_data=cb.base_cb.new(option=Menu.RECIPES, page=1)))
main_menu.add(InlineKeyboardButton(text='Вступить в КНМ',
                                   callback_data=cb.base_cb.new(option=Menu.APPLY, page=1)))
main_menu.add(InlineKeyboardButton(text='Предстоящие проекты',
                                   callback_data=cb.base_cb.new(option=Menu.PROJECTS, page=1)))

kb_close = InlineKeyboardButton(text='Закрыть',
                                callback_data=cb.base_cb.new(option=Menu.DELETE, page=1))
