from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.keyboards.menu import get_main_menu
from app.data.callbacks import BaseCallback
from app.data.states import Menu
from app.loader import _

menu_router = Router(name='menu')


@menu_router.message(Command('start', 'help', 'menu'))
async def handle_start_help(message: types.Message, state: FSMContext = None):
    await state.clear()
    return await message.answer(
        text=_('Приветствие'),
        reply_markup=get_main_menu())


@menu_router.callback_query(BaseCallback.filter(F.option == Menu.MAIN))
async def handle_back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    text = _('Приветствие')
    return await callback_query.message.edit_text(
        text=text,
        reply_markup=get_main_menu())
