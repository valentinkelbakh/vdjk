import asyncio
import logging
from urllib.parse import urljoin

from aiogram import Dispatcher
from aiogram.types import BotCommand

from app.loader import bot, dp
from app.utils.config import (WEBAPP_HOST, WEBAPP_PORT, WEBHOOK, WEBHOOK_HOST,
                              WEBHOOK_PATH)

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher: Dispatcher) -> None:
    logging.basicConfig(level=logging.INFO)
    if WEBHOOK:
        WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_PATH)
        logging.info("🟢 Bot launched as Serverless!")
        logging.info(f"webhook: {WEBHOOK_URL}")
        webhook = await dispatcher.bot.get_webhook_info()
        if webhook.url:
            await bot.delete_webhook()
        await bot.set_webhook(WEBHOOK_URL)
    else:
        logging.info("🟢 Bot launched!")

    commands_set = (
        ("/start", "Запустить VDJKate"),
        ("/holidays", "Праздники этнических немцев"),
        ("/recipes", "Традиционные немецкие блюда"),
        ("/apply", "Про СНМК"),
        ("/projects", "Предстоящие проекты"),
    )
    commands = []
    for command, description in commands_set:
        commands.append(BotCommand(command=command, description=description))
    await bot.set_my_commands(commands)


async def on_shutdown(dispatcher: Dispatcher) -> None:
    logging.warning("🟠 Bot shutdown...")
    if WEBHOOK:
        await bot.delete_webhook()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def bot_register() -> None:
    try:
        import app.handlers
        if WEBHOOK:
            raise NotImplementedError('Webhook is not implemented yet')
        else:
            dp.startup.register(on_startup)
            dp.shutdown.register(on_shutdown)
            await dp.start_polling(bot)
        return
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    asyncio.run(bot_register())
