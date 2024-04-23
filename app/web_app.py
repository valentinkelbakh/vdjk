import logging
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool

from app import bot
from app.loader import data, loop
from app.utils.config import DB_WEBHOOK_PASS
from app.utils.web import start_ngrok, start_webhook


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop.create_task(bot.bot_register())
    ngrok_url = await run_in_threadpool(start_ngrok)
    if ngrok_url:
        await run_in_threadpool(start_webhook, ngrok_url)
    await data.update_async()
    yield
    await bot.dp.stop_polling()


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)


@app.post("/webhook-endpoint")
async def webhook_endpoint(request: Request):
    response = await request.json()
    if response["webhook_pass"] == DB_WEBHOOK_PASS:
        loop.create_task(data.update_async, response["update_subject"])
        return Response(status_code=200, content="Webhook received")
    return HTTPException(status_code=403)


@app.get("/")
async def status():
    return Response(status_code=200)
