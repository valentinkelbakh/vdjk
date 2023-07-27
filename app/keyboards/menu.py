import re

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from app.data import callbacks as cb
from app.data.states import Menu

start_text = ("Привет, {}\n"
              "Вас приветствует бот VDJKate.\n"
              "Вы можете ознакомиться с моим функционалом, перейдя по ссылкам снизу!")


def get_back_btn(back_to):
    if back_to == Menu.Main:
        return InlineKeyboardButton(text='Назад', callback_data=cb.base_cb.new(option=Menu.Main, page=1))
    elif back_to == Menu.Recipes:
        return InlineKeyboardButton(text='Назад', callback_data=cb.base_cb.new(option=Menu.Recipes, page=1))
    elif back_to == Menu.Holidays:
        return InlineKeyboardButton(text='Назад', callback_data=cb.base_cb.new(option=Menu.Holidays, page=1))


main_menu = InlineKeyboardMarkup()
main_menu.add(InlineKeyboardButton(text='Праздники этнических немцев',
                                   callback_data=cb.base_cb.new(option=Menu.Holidays, page=1)))
main_menu.add(InlineKeyboardButton(text='Традиционные немецкие блюда',
                                   callback_data=cb.base_cb.new(option=Menu.Recipes, page=1)))
main_menu.add(InlineKeyboardButton(text='Вступить в КНМ',
                                   callback_data=cb.base_cb.new(option=Menu.Apply, page=1)))
main_menu.add(InlineKeyboardButton(text='Предстоящие проекты',
                                   callback_data=cb.base_cb.new(option=Menu.Projects, page=1)))

kb_close = InlineKeyboardButton(text='Закрыть',
                                callback_data=cb.base_cb.new(option=Menu.Delete, page=1))
