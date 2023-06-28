import logging, json, os

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

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Операция отменена.', reply_markup=types.ReplyKeyboardRemove())

@dp.errors_handler()
async def general_error_handler(update: types.Update, exception: Exception):
    match exception:
        case requests.exceptions.ConnectionError() | urllib3.exceptions.NewConnectionError():
            if 'callback_query' in update:
                chat_id = update.callback_query.message.chat.id
            elif 'message' in update:
                chat_id = update.message.chat.id
            logging.error(f'⭕ Нет подключения к базе данных')
            return await bot.send_message(chat_id, 'Нет соединения с базой данных')
        case exceptions.MessageNotModified:
            logging.error(f'⭕ Message not modified')
        # case PermissionError():
        #     state = dp.current_state()
        #     await state.finish()
        #     if 'callback_query' in update:
        #         try:
        #             await bot.edit_message_text(
        #                 chat_id=update.callback_query.message.chat.id,
        #                 message_id=update.callback_query.message.message_id,
        #                 text='Недостаточно прав для выполнения данного действия',
        #                 reply_markup=get_back()
        #             )
        #         except:
        #             pass
        #         #return await update.callback_query.answer('Недостаточно прав для выполнения данного действия')
        #     elif 'message' in update:
        #         return await update.message.answer('Недостаточно прав для выполнения данного действия')
        case _:
            logging.exception(f'⭕Exception {exception} Exception⭕')
            logging.error(f'\nTraceback ends⭕')
            return None

@dp.callback_query_handler(base_cb.filter(option=Menu.Main))
async def giveMenu(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    return await callback_query.message.answer("Тест", reply_markup=kb.base.main_menu)



@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Conversation's entry point
    """
    await state.finish()
    user_id = message.from_id

    return await message.answer("Тест", reply_markup=kb.base.main_menu)

@dp.callback_query_handler(base_cb.filter(option=Menu.Holidays))
async def handleOptionA(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):    
    # sample_data = [{
    #     'name': 'Праздник трех королей',
    #     'date': '2022-01-01',
    #     'link': 'https://wpv.kz/the-feast-of-the-three-kings-(dreik%C3%B6nigfest).html'
    # },
    # {
    #     'name': 'Праздник двух королей',
    #     'date': '2022-01-01',
    #     'link': 'https://wpv.kz/the-feast-of-the-three-kings-(dreik%C3%B6nigfest).html'
    # },
    # {
    #     'name': 'Праздник Четырех королей',
    #     'date': '2022-03-01',
    #     'link': 'https://wpv.kz/the-feast-of-the-three-kings-(dreik%C3%B6nigfest).html'
    # }]
    file_path = os.path.join(os.path.dirname(__file__), '../data/holidays.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    PAGE_SIZE = 5
    
    # def get_page(data, page_number, page_size):
    #     start_index = (page_number - 1) * page_size
    #     end_index = start_index + page_size
    #     return data[start_index:end_index]
    # if len(data) > PAGE_SIZE:
    #     data = get_page(data, 1, PAGE_SIZE)
    text = f'Немецкие праздники:\n'
    keyboard = InlineKeyboardMarkup()
    keyboard.add (kb.base.get_back_btn(Menu.Holidays))

    for each in data:
        #text += r'{}\n{}\n<a href="{}">{}<a/>\n'.format(each['name'], each['date'], each['link'], 'Подробнее')
        text += f"{each['name']}\n{each['date']}\n<a href='{each['link']}'>Подробнее</a>\n"

    
    return await callback_query.message.answer(text, parse_mode="HTML", reply_markup=keyboard)