from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject
from app.loader import stat_logger


class ActivityMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        handler_name = data['handler'].callback.__name__
        log_message = f'User @{user.username} ({user.id}) invoked handler {handler_name}'
        if isinstance(event, types.Message):
            log_message += f' with message: {event.text}'
        elif isinstance(event, types.CallbackQuery):
            log_message += f' with callback data: {event.data}'
        stat_logger.info(log_message)
        result = await handler(event, data)
        return result
