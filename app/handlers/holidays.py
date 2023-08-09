import json
import logging
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import keyboards as kb
from app.data import callbacks as cb
from app.data.states import Menu
from app.loader import dp

file_path = os.path.join(os.path.dirname(__file__), '../data/holidays.json')
holidays: dict = json.load(open(file_path, 'r', encoding='utf-8'))


@dp.message_handler(commands=['holidays'], state='*')
@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Holidays), state='*')
async def handleHolidays(update: types.CallbackQuery | types.Message, state: FSMContext):
    PAGE_SIZE = 5
    text = f'Немецкие праздники:\n\n'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(kb.menu.get_back_btn(Menu.Main))
    for each in holidays:
        keyboard.add(InlineKeyboardButton(text=each['name'], callback_data=cb.ext_cb.new(
            option=Menu.Holiday, page=1, data=each['id'])))
    if isinstance(update, types.CallbackQuery):
        return await update.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML', disable_web_page_preview=True)
    elif isinstance(update, types.Message):
        return await update.answer(
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML',
            disable_web_page_preview=True)


@dp.callback_query_handler(cb.ext_cb.filter(option=Menu.Holiday), state='*')
async def handleHoliday(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    holiday = next(
        (obj for obj in holidays if obj["id"] == int(callback_data['data'])), None)
    text = f"{holiday['name']}\n\n{holiday['description']}"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Подробнее', url=f'{holiday["link"]}'))
    keyboard.add(kb.menu.get_back_btn(Menu.Holidays))
    return await callback_query.message.edit_text(
        text=text,
        reply_markup=keyboard)


@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Closest), state='*')
async def handleClosest(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    logging.exception('Not implemented')
    return
    # text = 'До ближайшего немецкого праздника осталось: 103 дня (-ей)\nЭто праздник: Erntedankfest'
    # keyboard = InlineKeyboardMarkup()
    # keyboard.add(kb.base.get_back_btn(Menu.Main))
    # keyboard.add(InlineKeyboardButton('Перейти к празднику',
    #              callback_data=cb.ext_cb.new(option=Menu.Holiday, page=1, data=5)))
    # # return await callback_query.message.answer(text, reply_markup=keyboard)
