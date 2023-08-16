from aiogram.filters.callback_data import CallbackData


class BaseCallback(CallbackData, prefix="base"):
    option: str
    page: int


class ExtendedCallback(CallbackData, prefix="ext"):
    option: str
    page: int
    data: str
