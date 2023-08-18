from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import keyboards as kb
from app.data.callbacks import BaseCallback, ExtendedCallback
from app.data.states import Menu
from app.loader import dp, data


@dp.message(Command('projects'))
@dp.callback_query(BaseCallback.filter(F.option == Menu.PROJECTS))
async def handleProjects(update: types.CallbackQuery | types.Message, state: FSMContext):
    text = 'Предстоящие проекты СНМК:\n\n'
    builder = InlineKeyboardBuilder()
    builder.add(kb.menu.get_back_btn(Menu.MAIN))
    for each in data.projects:
        builder.add(InlineKeyboardButton(
            text=each['name'],
            callback_data=ExtendedCallback(option=Menu.PROJECT, page=1, data=str(each['id'])).pack()))
    builder.adjust(1)
    if isinstance(update, types.CallbackQuery):
        return await update.message.edit_text(
            text=text,
            reply_markup=builder.as_markup(),)
    elif isinstance(update, types.Message):
        return await update.answer(
            text=text,
            reply_markup=builder.as_markup(),)


@dp.callback_query(ExtendedCallback.filter(F.option == Menu.PROJECT))
async def handleProject(callback_query: types.CallbackQuery, callback_data: ExtendedCallback, state: FSMContext):
    project = data.project(int(callback_data.data))
    text = f"""{project['name']}\n{project['description']}\n"""
    keyboard = [
        [InlineKeyboardButton(text="Подать заявку", url=project['apply_link'])],
        [kb.menu.kb_close_btn]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return await callback_query.message.answer_photo(
        photo=project['img_link'],
        caption=text,
        reply_markup=reply_markup
    )
