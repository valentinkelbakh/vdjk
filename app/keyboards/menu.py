import re

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from app.data import callbacks as cb
from app.data.states import Menu

start_text = ("Вас приветствует бот VDJKate.\n\n"
              "VDJKate - бот, созданный в рамках Хакатона 2023 "
              "от союза немецкой молодежи Казахстана (Verband der Deutschen Jugend Kasachstans).\n"
              "Бот предоставляет информацию о традиционных немецких блюдах"
              " и праздниках, а также о предстоящих проектах VDJK.\n\n"
              "Выберите, что вам интересно:")


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
main_menu.add(InlineKeyboardButton(text='Про СНМК',
                                   callback_data=cb.base_cb.new(option=Menu.APPLY, page=1)))
main_menu.add(InlineKeyboardButton(text='Предстоящие проекты',
                                   callback_data=cb.base_cb.new(option=Menu.PROJECTS, page=1)))

kb_close = InlineKeyboardButton(text='Закрыть',
                                callback_data=cb.base_cb.new(option=Menu.DELETE, page=1))
