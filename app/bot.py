import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand

from app.loader import bot, dp, server, WEBHOOK_URL
from app.utils.config import WEBHOOK
from pyngrok import ngrok
from app.utils.webhook import start_webhook
logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher: Dispatcher) -> None:
    logging.basicConfig(level=logging.INFO)
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
            ngrok_connect = ngrok.connect(8080)
            WEBHOOK_URL = ngrok_connect.public_url
            print(f'Public URL: {ngrok_connect.public_url}\n')
            if start_webhook(WEBHOOK_URL):
                print("Webhook started\n")
            await dp.start_polling(bot)
        return
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception(e)


async def hook_server():
    await server.serve()


async def main():
    bot_task = asyncio.create_task(bot_register())
    hook_task = asyncio.create_task(hook_server())
    await asyncio.gather(bot_task, hook_task)


if __name__ == '__main__':
    asyncio.run(main())
