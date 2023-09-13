from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app import keyboards as kb
from app.data.callbacks import BaseCallback
from app.data.states import Menu

menu_router = Router(name='menu')


@menu_router.message(Command('start', 'help', 'menu'))
async def handle_start_help(message: types.Message, state: FSMContext = None):
    await state.clear()
    text = kb.menu.start_text
    return await message.answer(text=text, reply_markup=kb.menu.main_menu)


@menu_router.callback_query(BaseCallback.filter(F.option == Menu.MAIN))
async def handle_back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    text = kb.menu.start_text
    return await callback_query.message.edit_text(text=text, reply_markup=kb.menu.main_menu)
