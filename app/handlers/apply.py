from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import keyboards as kb
from app.data import callbacks as cb
from app.data.states import Menu
from app.loader import dp


@dp.message(Command('apply'))
@dp.callback_query(cb.BaseCallback.filter(F.option==Menu.APPLY))
async def handleApply(update: types.CallbackQuery | types.Message, state: FSMContext):
    text = 'Verband der Deutschen Jugend Kasachstans (Союз немецкой молодежи Казахстана) был создан в феврале 1996 года и объединяет клубы немецкой молодежи, функционирующие на территории Казахстана.\n\nЦелью СНМК является поддержка немецкой молодежи Казахстана для ее самореализации в различных сферах жизни, развитие конкурентоспособности молодого человека с сохранением этнической идентичности.\n\nЕжегодно СНМК реализует проекты, направленные на консолидацию молодежи, изучение и совершенствование немецкого языка, сохранения истории и культуры немцев Казахстана, развитие социальной ответственности у молодежи, укрепление партнерских отношений с другими молодежными организациями.\n\nНа данный момент по территории Казахстана существует 20 клубов и с каждым годом это число растёт!'
    apply_form_link = r'https://docs.google.com/forms/d/e/1FAIpQLSfdxmwmnS9tmH5yaY7pfO_0A4Ssk7SwDlz-DpDRfdvUsjv91g/viewform'
    keyboard = [
        [InlineKeyboardButton(text='Подать заявку на вступление', url=apply_form_link)],
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
