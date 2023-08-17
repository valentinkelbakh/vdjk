from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import keyboards as kb
from app.data.callbacks import BaseCallback, ExtendedCallback
from app.data.states import Menu
from app.loader import dp, data


@dp.message(Command('holidays'))
@dp.callback_query(BaseCallback.filter(F.option == Menu.HOLIDAYS))
async def handleHolidays(update: types.CallbackQuery | types.Message, state: FSMContext):
    PAGE_SIZE = 5
    text = f'Немецкие праздники:\n\n'
    builder = InlineKeyboardBuilder()
    builder.add(kb.menu.get_back_btn(Menu.MAIN))
    for each in data.holidays:
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
    holiday = data.holiday(int(callback_data.data))
    text = f"{holiday['name']}\n\n{holiday['description']}"
    keyboard = [
        [InlineKeyboardButton(text='Подробнее', url=f'{holiday["link"]}')],
        [kb.menu.get_back_btn(Menu.HOLIDAYS)]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return await callback_query.message.edit_text(
        text=text,
        reply_markup=reply_markup)
