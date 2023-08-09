import logging
import time
import pytz
from datetime import datetime
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class MyLoggingMiddleware(BaseMiddleware):
    def __init__(self, logger=__name__):
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)
        self.logger = logger
        super(MyLoggingMiddleware, self).__init__()

    def check_timeout(self, obj):
        start = obj.conf.get('_start', None)
        if start:
            del obj.conf['_start']
            return round((time.time() - start) * 1000)
        return -1

    async def on_pre_process_update(self, update: types.Update, data: dict):
        update.conf['_start'] = time.time()
        current_time = current_time = pytz.timezone(
            'Asia/Almaty').localize(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        if update.callback_query:
            self.logger.info(
                f"{current_time}:Received callback query [ID:{update.update_id}] from chat [{update.callback_query.message.chat.id}] ({update.callback_query.message.chat.mention})")
        elif update.message:
            self.logger.info(
                f"{current_time}:Received message [ID:{update.update_id}] from chat [{update.message.chat.id}] ({update.message.chat.mention})")

    async def on_post_process_update(self, update: types.Update, result, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.info(f"Update [ID:{update.update_id}] processed in {timeout} ms")
