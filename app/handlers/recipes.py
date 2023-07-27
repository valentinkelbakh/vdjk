import json
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from app import keyboards as kb
from app.data import callbacks as cb
from app.data.states import Menu
from app.loader import dp


@dp.message_handler(commands=['recipes'], state='*')
@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Recipes), state='*')
async def handleRecipes(update: types.CallbackQuery | types.Message, state: FSMContext):
    file_path = os.path.join(os.path.dirname(__file__), '../data/recipes.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    text = 'Список блюд:\n'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(kb.menu.get_back_btn(Menu.Main))
    for each in data:
        keyboard.add(InlineKeyboardButton(
            text=each['name'],
            callback_data=cb.ext_cb.new(option=Menu.Recipe, page=1, data=each['id'])))
    if isinstance(update, types.CallbackQuery):
        return await update.message.edit_text(
            text=text,
            reply_markup=keyboard,)
    elif isinstance(update, types.Message):
        return await update.answer(
            text=text,
            reply_markup=keyboard,)


@dp.callback_query_handler(cb.ext_cb.filter(option=Menu.Recipe), state='*')
async def handleRecipe(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    file_path = os.path.join(os.path.dirname(__file__), '../data/recipes.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    receipt = next(
        (obj for obj in data if obj["id"] == int(callback_data['data'])), None)

    text = f"{receipt['name']}\n\n{receipt['description']}"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        "Рецепт", url=receipt['recipe-link']))

    keyboard.add(kb.menu.kb_close)
    return await callback_query.message.answer_photo(
        photo=receipt['img-link'],
        caption=text,
        reply_markup=keyboard,
    )
