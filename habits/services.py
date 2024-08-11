import requests
from django.conf import settings

URL = settings.TELEGRAM_URL
TOKEN = settings.TOKEN_BOT


def send_message(text, chat_id):
    """
    Отправляет сообщение через Telegram бот
    """
    url = f'{URL}{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, data=payload)
    # response = requests.post(url, data=payload)
    # return response.json()
