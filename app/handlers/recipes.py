from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import keyboards as kb
from app.data.callbacks import BaseCallback, ExtendedCallback
from app.data.states import Menu
from app.loader import data
from app.utils.tools import trim_for_button, trim_for_caption
from app.loader import _
recipes_router = Router(name='recipes')


@recipes_router.message(Command('recipes'))
@recipes_router.callback_query(BaseCallback.filter(F.option == Menu.RECIPES))
async def handleRecipes(update: types.CallbackQuery | types.Message, state: FSMContext):
    text = _('Традиционные немецкие блюда:')
    builder = InlineKeyboardBuilder()
    builder.add(kb.menu.get_back_btn(Menu.MAIN))
    for each in data.recipes:
        builder.button(
            text=trim_for_button(each['name']),
            callback_data=ExtendedCallback(option=Menu.RECIPE, page=1, data=str(each['id'])).pack())
    builder.adjust(1)
    if isinstance(update, types.CallbackQuery):
        return await update.message.edit_text(
            text=text,
            reply_markup=builder.as_markup(column_count=1),)
    elif isinstance(update, types.Message):
        return await update.answer(
            text=text,
            reply_markup=builder.as_markup(column_count=1),)


@recipes_router.callback_query(ExtendedCallback.filter(F.option == Menu.RECIPE))
async def handleRecipe(callback_query: types.CallbackQuery, callback_data: ExtendedCallback, state: FSMContext):
    recipe = data.recipe(int(callback_data.data))
    if not recipe:
        return await callback_query.answer(_('Информация недоступна'))
    text = _("{recipe[name]}\n\n{recipe[description]}").format(
        recipe=recipe
    )
    keyboard = [
        [InlineKeyboardButton(text=_("Рецепт"), url=recipe['recipe_link'])],
        [kb.menu.get_close_btn()]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return await callback_query.message.answer_photo(
        photo=recipe['img_link'],
        caption=trim_for_caption(text),
        reply_markup=reply_markup,
    )
