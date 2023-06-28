import logging
import json
import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from app.loader import dp, bot
from app.data import callbacks as cb
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

import logging
import requests.exceptions
import urllib3.exceptions
from aiogram.utils import exceptions

from app.data.states import Menu
from app import keyboards as kb
from app.utils import tools
from datetime import datetime, timedelta


@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Delete))
async def delete_message(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        logging.error(e)


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
            logging.error(
                f'⭕ Нет подключения к базе данных')
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


@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Main), state='*')
async def giveMenu(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    text = f"Привет, {(callback_query.message.chat.first_name)}\n\
Вас приветствует бот VDJKate. \n\
Вы можете ознакомиться с моим функционалом, перейдя по ссылкам снизу!\
"
    return await tools.update_or_send(
        callback_query.message,
        text,
        kb.base.main_menu
    )


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):

    await state.finish()
    user_id = message.from_id
    text = f"Привет, {(message.chat.first_name)}\n\
Вас приветствует бот VDJKate. \n\
Вы можете ознакомиться с моим функционалом, перейдя по ссылкам снизу!\
"
    return await message.answer(text, reply_markup=kb.base.main_menu)
    # return await tools.update_or_send(message, text, kb.base.main_menu)


@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Holidays), state='*')
async def handleHolidays(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    file_path = os.path.join(os.path.dirname(
        __file__), '../data/holidays.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    PAGE_SIZE = 5

    # def get_page(data, page_number, page_size):
    #     start_index = (page_number - 1) * page_size
    #     end_index = start_index + page_size
    #     return data[start_index:end_index]
    # if len(data) > PAGE_SIZE:
    #     data = get_page(data, 1, PAGE_SIZE)
    text = f'Немецкие праздники:\n\n'
    page = callback_data.get('page', 1)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(kb.base.get_back_btn(Menu.Main))
    keyboard.add(InlineKeyboardButton(text='Ближайший праздник',
                 callback_data=cb.ext_cb.new(option=Menu.Holiday, page=page, data=5)))
    for each in data:
        # text += r'{}\n{}\n<a href="{}">{}<a/>\n'.format(each['name'], each['date'], each['link'], 'Подробнее')
        keyboard.add(InlineKeyboardButton(text=each['name'], callback_data=cb.ext_cb.new(option=Menu.Holiday, page=1, data=each['id'])))
        # prepared = f"""{each['name']}\n{each['date']}\n<a href="{each['link']}">Подробнее</a>\n\n"""
        # text += prepared
    
    
    return await callback_query.message.answer(text, reply_markup=keyboard, parse_mode='HTML', disable_web_page_preview=True)
    # return await tools.update_or_send(callback_query.message, text, keyboard,parse_mode='HTML', disable_web_page_preview=True)


@dp.callback_query_handler(cb.ext_cb.filter(option=Menu.Holiday), state='*')
async def handleHoliday(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    file_path = os.path.join(os.path.dirname(
        __file__), '../data/holidays.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    holiday = next(
        (obj for obj in data if obj["id"] == int(callback_data['data'])), None)
    text = f"{holiday['name']}\n\n{holiday['description']}"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Подробнее', url=f'{holiday["link"]}'))
    keyboard.add(kb.base.kb_close)

    return await callback_query.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Recipes), state='*')
async def handleReceipts(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    file_path = os.path.join(os.path.dirname(__file__), '../data/recipes.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    page = callback_data.get('page', 1)
    text = 'Список блюд:\n'

    keyboard = InlineKeyboardMarkup()
    keyboard.add(kb.base.get_back_btn(Menu.Main))
    for each in data:
        keyboard.add(InlineKeyboardButton(
            text=each['name'],
            callback_data=cb.ext_cb.new(option=Menu.Recipe, page=page, data=each['id'])))

    return await callback_query.message.answer(text, reply_markup=keyboard)

    # return await bot.edit_message_text(
    #     chat_id=callback_query.message.chat.id,
    #     message_id=callback_query.message.message_id,
    #     text=text,
    #     reply_markup=keyboard
    # )

    PAGE_SIZE = 5


@dp.callback_query_handler(cb.ext_cb.filter(option=Menu.Recipe), state='*')
async def handleReceipt(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    file_path = os.path.join(os.path.dirname(__file__), '../data/recipes.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    receipt = next(
        (obj for obj in data if obj["id"] == int(callback_data['data'])), None)

    text = f"{receipt['name']}\n\n{receipt['description']}"
    # text = f"""{receipt['name']}\n{receipt['description']}\n<a href="{receipt['recipe-link']}">Рецепт</a>\n\n"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        "Рецепт", url=receipt['recipe-link']))
    keyboard.add(kb.base.kb_close)
    return await callback_query.message.answer_photo(
        photo=receipt['img-link'],
        caption=text,
        reply_markup=keyboard,
        # parse_mode="HTML"
    )



@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Apply), state='*')
async def handleApply(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = 'Verband der Deutschen Jugend Kasachstans (Союз немецкой молодежи Казахстана) был создан в феврале 1996 года и объединяет клубы немецкой молодежи, функционирующие на территории Казахстана.\n\nЦелью СНМК является поддержка немецкой молодежи Казахстана для ее самореализации в различных сферах жизни, развитие конкурентоспособности молодого человека с сохранением этнической идентичности.\n\nЕжегодно СНМК реализует проекты, направленные на консолидацию молодежи, изучение и совершенствование немецкого языка, сохранения истории и культуры немцев Казахстана, развитие социальной ответственности у молодежи, укрепление партнерских отношений с другими молодежными организациями.\n\nНа данный момент по территории Казахстана существует 20 клубов и с каждым годом это число растёт!'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Подать заявку',
                 url=r'https://docs.google.com/forms/d/e/1FAIpQLSfdxmwmnS9tmH5yaY7pfO_0A4Ssk7SwDlz-DpDRfdvUsjv91g/viewform'))
    keyboard.add(kb.base.get_back_btn(Menu.Main))
    return await callback_query.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Projects), state='*')
async def handleProjects(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = 'Проекты:\n\n'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(kb.base.get_back_btn(Menu.Main))
    file_path = os.path.join(os.path.dirname(__file__), '../data/projects.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(kb.base.get_back_btn(Menu.Main))
    for each in data:
        keyboard.add(InlineKeyboardButton(
            text=each['name'],
            callback_data=cb.ext_cb.new(option=Menu.Project, page=1, data=each['id'])))
    
    return await callback_query.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(cb.ext_cb.filter(option=Menu.Project), state='*')
async def handleProject(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    file_path = os.path.join(os.path.dirname(__file__), '../data/projects.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    project = next(
        (obj for obj in data if obj["id"] == int(callback_data['data'])), None)

    text = f"""{project['name']}\n{project['description']}\n"""
    # text = f"""{project['name']}\n{project['description']}\n<a href="{project['link']}">Подробнее</a>\n\n"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Подать заявку", url=project['apply-link']))
    keyboard.add(kb.base.kb_close)
    return await callback_query.message.answer_photo(
        photo=project['img-link'],
        caption=text,
        reply_markup=keyboard
    )
from aiogram import utils
utils.exceptions.BadRequest

# @dp.callback_query_handler(cb.base_cb.filter(option=Menu.Closest), state='*')
# async def handleClosest(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
#     text = 'Ваша инфа о ближайшем празднике'
#     keyboard = InlineKeyboardMarkup()
#     keyboard.add(kb.base.get_back_btn(Menu.Main))
#     keyboard.add(InlineKeyboardButton('Перейти к празднику', callback_data=cb.ext_cb.new(option=Menu.Holiday, page=1)))
#     return await callback_query.message.answer(text, reply_markup=keyboard)
#     # Get the current month and day
    
