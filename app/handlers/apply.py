from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from app import keyboards as kb
from app.data import callbacks as cb
from app.data.states import Menu
from app.loader import dp


@dp.message_handler(commands=['apply'], state='*')
@dp.callback_query_handler(cb.base_cb.filter(option=Menu.Apply), state='*')
async def handleApply(update: types.CallbackQuery | types.Message, state: FSMContext):
    text = 'Verband der Deutschen Jugend Kasachstans (Союз немецкой молодежи Казахстана) был создан в феврале 1996 года и объединяет клубы немецкой молодежи, функционирующие на территории Казахстана.\n\nЦелью СНМК является поддержка немецкой молодежи Казахстана для ее самореализации в различных сферах жизни, развитие конкурентоспособности молодого человека с сохранением этнической идентичности.\n\nЕжегодно СНМК реализует проекты, направленные на консолидацию молодежи, изучение и совершенствование немецкого языка, сохранения истории и культуры немцев Казахстана, развитие социальной ответственности у молодежи, укрепление партнерских отношений с другими молодежными организациями.\n\nНа данный момент по территории Казахстана существует 20 клубов и с каждым годом это число растёт!'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Подать заявку',
                 url=r'https://docs.google.com/forms/d/e/1FAIpQLSfdxmwmnS9tmH5yaY7pfO_0A4Ssk7SwDlz-DpDRfdvUsjv91g/viewform'))
    keyboard.add(kb.menu.get_back_btn(Menu.Main))

    if isinstance(update, types.CallbackQuery):
        return await update.message.edit_text(
            text=text,
            reply_markup=keyboard)
    elif isinstance(update, types.Message):
        return await update.answer(
            text=text,
            reply_markup=keyboard)
