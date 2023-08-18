

from app.loader import data
from app.utils.config import WEBHOOK_PASS, DB_API_URL
from fastapi import FastAPI
from fastapi import Request
from app.loader import WEBHOOK_URL
import requests
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
        return "Webhook received", 200
    return "", 404


@app.get('/')
async def status():
    print('Webhook started\n')
    return 'All set'


def start_webhook(url):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "content": WEBHOOK_PASS,
        'webhook_url': url
    }

    try:
        response = requests.post(f'{DB_API_URL}/set-webhook/', headers=headers, json=payload)
    except:
        response = None
    if response and response.status_code == 200:
        return True
    return False
