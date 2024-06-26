import logging

import requests
from pyngrok import ngrok

from app.utils.config import API_LOGIN, API_PASSWORD, API_URL, DB_WEBHOOK_PASS


def start_webhook(url):
    headers = {"Content-Type": "application/json"}
    payload = {"webhook_pass": DB_WEBHOOK_PASS, "webhook_url": url}

    try:
        response = requests.post(
            f"{API_URL}/set-webhook/",
            headers=headers,
            json=payload,
            auth=(API_LOGIN, API_PASSWORD),
        )
    except BaseException as error:
        logging.error(f"⭕ Webhook not set {error} ⭕")
    if response and response.status_code == 200:
        logging.info(f"🔵 URL for webhook set")
    else:
        logging.warning(f"⭕ Webhook not delivered {response} ⭕")


def start_ngrok() -> str:
    ngrok_logger = logging.getLogger("pyngrok")
    ngrok_logger.setLevel(logging.WARNING)
    try:
        ngrok_connect = ngrok.connect(8080)
    except BaseException as error:
        logging.error(f"⭕ Ngrok not started: \n{error} ⭕")
        return ""
    logging.info(f"🔵 Ngrok public URL: {ngrok_connect.public_url}")
    return ngrok_connect.public_url
