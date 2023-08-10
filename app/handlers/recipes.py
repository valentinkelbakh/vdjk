import json
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import keyboards as kb
from app.data import callbacks as cb
from app.data.states import Menu
from app.loader import dp

file_path = os.path.join(os.path.dirname(__file__), '../data/recipes.json')
recipes = json.load(open(file_path, 'r', encoding='utf-8'))


@dp.message_handler(commands=['recipes'], state='*')
@dp.callback_query_handler(cb.base_cb.filter(option=Menu.RECIPES), state='*')
async def handleRecipes(update: types.CallbackQuery | types.Message, state: FSMContext):
    text = 'Традиционные немецкие блюда:\n'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(kb.menu.get_back_btn(Menu.MAIN))
    for each in recipes:
        keyboard.add(InlineKeyboardButton(
            text=each['name'],
            callback_data=cb.ext_cb.new(option=Menu.RECIPE, page=1, data=each['id'])))
    if isinstance(update, types.CallbackQuery):
        return await update.message.edit_text(
            text=text,
            reply_markup=keyboard,)
    elif isinstance(update, types.Message):
        return await update.answer(
            text=text,
            reply_markup=keyboard,)


@dp.callback_query_handler(cb.ext_cb.filter(option=Menu.RECIPE), state='*')
async def handleRecipe(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    recipe = next(
        (obj for obj in recipes if obj["id"] == int(callback_data['data'])), None)

    text = f"{recipe['name']}\n\n{recipe['description']}"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        "Рецепт", url=recipe['recipe-link']))

    keyboard.add(kb.menu.kb_close)
    return await callback_query.message.answer_photo(
        photo=recipe['img-link'],
        caption=text,
        reply_markup=keyboard,
    )
