from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import keyboards as kb
from app.data import callbacks as cb
from app.data.states import Menu
from app.loader import _

apply_router = Router(name='apply')


@apply_router.message(Command('apply'))
@apply_router.callback_query(cb.BaseCallback.filter(F.option == Menu.APPLY))
async def handleApply(update: types.CallbackQuery | types.Message, state: FSMContext):
    text = _('Про СНМК, текст')
    keyboard = [
        [InlineKeyboardButton(text=_('Подать заявку'), url=_('Подать заявку, ссылка'))],
        [kb.menu.get_back_btn(Menu.MAIN)]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    if isinstance(update, types.CallbackQuery):
        return await update.message.edit_text(
            text=text,
            reply_markup=reply_markup)
    elif isinstance(update, types.Message):
        return await update.answer(
            text=text,
            reply_markup=reply_markup)
