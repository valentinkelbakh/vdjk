from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
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
        stat_logger.info(f'User @{user.username} ({user.id}) invoked handler {handler_name}')
        result = await handler(event, data)
        return result
