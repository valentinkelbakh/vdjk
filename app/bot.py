import logging
from urllib.parse import urljoin

from aiogram import Dispatcher, executor
from aiogram.types import BotCommand

from app.loader import bot, dp
from app.utils.config import (SERVERLESS, WEBAPP_HOST, WEBAPP_PORT,
                              WEBHOOK_HOST, WEBHOOK_PATH)

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher: Dispatcher) -> None:
    if SERVERLESS:
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
        ("/apply", "Вступить в КНМ"),
        ("/projects", "Предстоящие проекты"),
    )
    commands = []
    for command, description in commands_set:
        commands.append(BotCommand(command=command, description=description))
    await dispatcher.bot.set_my_commands(commands)

    aiogram_logger = logging.getLogger('aiogram')
    aiogram_logger.setLevel(logging.WARNING)


async def on_shutdown(dispatcher: Dispatcher) -> None:
    logging.warning("🟠 Bot shutdown...")
    if SERVERLESS is True:
        await bot.delete_webhook()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def bot_register(webhook: bool = False) -> None:
    try:
        import app.handlers
        import app.middlewares

        if SERVERLESS and webhook:
            executor.start_webhook(
                dispatcher=dp,
                webhook_path=WEBHOOK_PATH,
                on_startup=on_startup,
                on_shutdown=on_shutdown,
                skip_updates=True,
                host=WEBAPP_HOST,
                port=WEBAPP_PORT,
            )
        else:
            executor.start_polling(
                dp,
                skip_updates=True,
                on_startup=on_startup,
                on_shutdown=on_shutdown,
            )
        return
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    bot_register(True)
