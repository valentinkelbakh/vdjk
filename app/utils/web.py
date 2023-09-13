import logging

import requests
from pyngrok import ngrok

from app.utils.config import DB_API_URL, DB_LOGIN, DB_PASSWORD, WEBHOOK_PASS


def start_webhook(url):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "content": WEBHOOK_PASS,
        'webhook_url': url
    }

    try:
        response = requests.post(f'{DB_API_URL}/set-webhook/',
                                 headers=headers,
                                 json=payload,
                                 auth=(DB_LOGIN, DB_PASSWORD)
                                 )
    except:
        response = None
    if response and response.status_code == 200:
        logging.info(f'🔵 URL for webhook set')


def start_ngrok() -> str:
    ngrok_logger = logging.getLogger('pyngrok')
    ngrok_logger.setLevel(logging.WARNING)
    ngrok_connect = ngrok.connect(8080)
    logging.info(f'🔵Public URL: {ngrok_connect.public_url}')
    return ngrok_connect.public_url
