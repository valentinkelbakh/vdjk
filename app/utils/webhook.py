

from app.loader import data
from app.utils.config import WEBHOOK_PASS
from fastapi import FastAPI
from fastapi import Request

app = FastAPI()
""" The purpose of this app is to handle POST request sent to this endpoint.
    Request notifies about update in database."""

@app.post('/webhook-endpoint')
async def webhook_endpoint(request: Request):
    # Handle the incoming webhook data here
    print(request)
    _data = await request.json()
    if _data['content'] == WEBHOOK_PASS:
        print(f"Received webhook🟡")
        data.update()
        return "Webhook received"
    return "", 404
    