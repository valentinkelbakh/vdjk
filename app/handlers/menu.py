
from aiogram import types
from aiogram.dispatcher import FSMContext

from app import keyboards as kb
from app.data import callbacks as cb
from app.data.states import Menu
from app.loader import dp


@dp.message_handler(commands=['start', 'help', 'menu'], state='*')
async def handle_start_help(message: types.Message, state: FSMContext = None):
    await state.finish()
    text = kb.menu.start_text.format(message.chat.first_name)
    return await message.answer(text=text, reply_markup=kb.menu.main_menu)


@dp.callback_query_handler(cb.base_cb.filter(option=Menu.MAIN), state='*')
async def handle_back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    text = kb.menu.start_text.format(callback_query.message.chat.first_name)
    return await callback_query.message.edit_text(text=text, reply_markup=kb.menu.main_menu)
