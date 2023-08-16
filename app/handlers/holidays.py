import json
import logging
import os

from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import keyboards as kb
from app.data.callbacks import BaseCallback, ExtendedCallback
from app.data.states import Menu
from app.loader import dp

file_path = os.path.join(os.path.dirname(__file__), '../data/holidays.json')
holidays: dict = json.load(open(file_path, 'r', encoding='utf-8'))


@dp.message(Command('holidays'))
@dp.callback_query(BaseCallback.filter(F.option == Menu.HOLIDAYS))
async def handleHolidays(update: types.CallbackQuery | types.Message, state: FSMContext):
    PAGE_SIZE = 5
    text = f'Немецкие праздники:\n\n'
    builder = InlineKeyboardBuilder()
    builder.add(kb.menu.get_back_btn(Menu.MAIN))
    for each in holidays:
        builder.add(InlineKeyboardButton(
            text=each['name'],
            callback_data=ExtendedCallback(option=Menu.HOLIDAY, page=1, data=str(each['id'])).pack()))
    builder.adjust(1)
    if isinstance(update, types.CallbackQuery):
        return await update.message.edit_text(
            text=text,
            reply_markup=builder.as_markup(),
            parse_mode='HTML', disable_web_page_preview=True)
    elif isinstance(update, types.Message):
        return await update.answer(
            text=text,
            reply_markup=builder.as_markup(),
            parse_mode='HTML',
            disable_web_page_preview=True)


@dp.callback_query(ExtendedCallback.filter(F.option == Menu.HOLIDAY))
async def handleHoliday(callback_query: types.CallbackQuery, callback_data: ExtendedCallback, state: FSMContext):
    holiday = next(
        (obj for obj in holidays if obj["id"] == int(callback_data.data)), None)
    text = f"{holiday['name']}\n\n{holiday['description']}"
    keyboard = [
        [InlineKeyboardButton(text='Подробнее', url=f'{holiday["link"]}')],
        [kb.menu.get_back_btn(Menu.HOLIDAYS)]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return await callback_query.message.edit_text(
        text=text,
@dp.callback_query_handler(cb.base_cb.filter(option=Menu.CLOSEST), state='*')
async def handleClosest(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    logging.exception('Not implemented')
    return
    # text = 'До ближайшего немецкого праздника осталось: 103 дня (-ей)\nЭто праздник: Erntedankfest'
    # keyboard = InlineKeyboardMarkup()
    # keyboard.add(kb.base.get_back_btn(Menu.Main))
    # keyboard.add(InlineKeyboardButton('Перейти к празднику',
    #              callback_data=cb.ext_cb.new(option=Menu.Holiday, page=1, data=5)))
    # # return await callback_query.message.answer(text, reply_markup=keyboard)
        reply_markup=reply_markup)
