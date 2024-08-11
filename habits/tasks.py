from datetime import datetime, timedelta
import requests
from celery import shared_task
from django.conf import settings
from habits.models import Habits
from users.models import User
from .services import send_message

TOKEN = settings.TOKEN_BOT
URL = settings.TELEGRAM_URL


@shared_task
def send_tg_message():
    """
    Отправка сообщения в телеграм
    """
    time_now = datetime.now().time()
    start_time = (datetime.combine(datetime.today(), time_now) - timedelta(minutes=10)).time()
    finish_time = (datetime.combine(datetime.today(), time_now) + timedelta(minutes=10)).time()

    habits = Habits.objects.filter(time__gte=start_time, time__lte=finish_time)

    updates = get_updates()
    if updates['ok']:
        parser_updates(updates['result'])

    for h in habits:
        action = h.action
        place = h.place
        time = h.time
        time_to_complete = h.time_to_complete
        owner = h.owner
        chat_id = owner.telegram_id

        if chat_id:
            text = (f'Привычка: {action} '
                    f'в {place} '
                    f'время: {time} '
                    f'на протяжении {time_to_complete} минут')
            send_message(text, chat_id)
            h.time = (datetime.combine(datetime.today(), h.time) + timedelta(days=h.periodicity)).time()
            h.save()


def get_updates():
    """
    Получает обновления от Telegram
    """
    response = requests.get(f'{URL}{TOKEN}/getUpdates')
    return response.json()


def parser_updates(updates):
    for update in updates:
        chat = update['message']['chat']
        username = chat.get('username')
        chat_id = chat['id']

        if username:
            try:
                user = User.objects.get(telegram_nik=username)
                user.chat_id = chat_id
                user.save()
            except User.DoesNotExist:
                continue
