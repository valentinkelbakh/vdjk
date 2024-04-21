from aiogram.filters.callback_data import CallbackData


class BaseCallback(CallbackData, prefix="post", sep="|"):
    option: str
    page: int


class ExtendedCallback(CallbackData, prefix="post", sep="|"):
    option: str
    page: int
    data: str
