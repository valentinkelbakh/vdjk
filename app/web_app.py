import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool

from app import bot
from app.loader import data
from app.utils.config import DB_WEBHOOK_PASS
from app.utils.web import start_ngrok, start_webhook

loop = asyncio.get_event_loop()


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop.create_task(bot.bot_register())
    ngrok_url = await run_in_threadpool(start_ngrok)
    loop.run_in_executor(None, start_webhook, ngrok_url)
    yield
    await bot.dp.stop_polling()


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)


@app.post("/webhook-endpoint")
async def webhook_endpoint(request: Request, background_tasks: BackgroundTasks):
    global data
    _data = await request.json()
    if _data["webhook_pass"] == DB_WEBHOOK_PASS:
        background_tasks.add_task(
            data.update_async, update_subject=_data["update_subject"]
        )
        # background_tasks.add_task(data.save_data)
        logging.info("🔵Webhook received, updating..")
        return Response(status_code=200, content="Webhook received")
    return HTTPException(status_code=403)


@app.get("/")
async def status():
    return Response(status_code=200)
