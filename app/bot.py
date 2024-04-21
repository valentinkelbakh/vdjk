import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand

from app.handlers import routers
from app.loader import bot, dp, i18n_middleware
from app.utils.config import WEBHOOK
from app.utils.middlewares import ActivityMiddleware

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(name)s:%(asctime).19s:%(message)s"
)


async def on_startup(dispatcher: Dispatcher) -> None:
    logging.info("🟢 Bot launching...")

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
    await dispatcher.storage.close()


async def bot_register() -> None:
    try:
        if WEBHOOK:
            raise NotImplementedError("Webhook is not implemented yet")
        else:
            for router in routers:
                router.message.middleware(ActivityMiddleware())
                router.callback_query.middleware(ActivityMiddleware())
                i18n_middleware.setup(router)
            dp.include_routers(*routers)
            dp.startup.register(on_startup)
            dp.shutdown.register(on_shutdown)
            await dp.start_polling(bot)
        return
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt")
        pass
    except BaseException as e:
        logging.exception(e)
