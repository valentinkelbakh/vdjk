import json
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from app import keyboards as kb
from app.data import callbacks as cb
from app.data.states import Menu
from app.loader import dp


@dp.message_handler(commands=['projects'], state='*')
@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Projects), state='*')
async def handleProjects(update: types.CallbackQuery | types.Message, state: FSMContext):
    text = 'Проекты:\n\n'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(kb.menu.get_back_btn(Menu.Main))
    file_path = os.path.join(os.path.dirname(__file__), '../data/projects.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(kb.menu.get_back_btn(Menu.Main))
    for each in data:
        keyboard.add(InlineKeyboardButton(
            text=each['name'],
            callback_data=cb.ext_cb.new(option=Menu.Project, page=1, data=each['id'])))
    if isinstance(update, types.CallbackQuery):
        return await update.message.edit_text(
            text=text,
            reply_markup=keyboard,)
    elif isinstance(update, types.Message):
        return await update.answer(
            text=text,
            reply_markup=keyboard,)


@dp.callback_query_handler(cb.ext_cb.filter(option=Menu.Project), state='*')
async def handleProject(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    file_path = os.path.join(os.path.dirname(__file__), '../data/projects.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    project = next(
        (obj for obj in data if obj["id"] == int(callback_data['data'])), None)

    text = f"""{project['name']}\n{project['description']}\n"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Подать заявку", url=project['apply-link']))
    keyboard.add(kb.menu.kb_close)
    return await callback_query.message.answer_photo(
        photo=project['img-link'],
        caption=text,
        reply_markup=keyboard
    )
