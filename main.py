import time
import pytz
import requests
import datetime

from config import *


url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
telegram_queue = []
moscow_tz = pytz.timezone('Europe/Moscow')


def send_telegram_message(text):
    """ Сохраняем сообщение в очереди на отправку """
    moscow_time = moscow_tz.localize(datetime.datetime.now())
    text = f"**Яндекс Облако**\n[{moscow_time.strftime("%d.%m.%Y %H:%M")} (Мск)] {text}"

    # Формируем словарь прокси для библиотеки requests
    for tg_chat_id in TG_CHAT_IDS:
        telegram_queue.append((tg_chat_id, text))

def push_telegram_messages():
    """Отправляет уведомление в Telegram."""
    telegram_queue_copy = telegram_queue.copy()
    telegram_queue.clear()

    for tg_chat_id, text in telegram_queue_copy:
        payload = {
            'chat_id': tg_chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Ошибка при отправке в Telegram чат {tg_chat_id}, попробую отправить позже: {e}")
            telegram_queue.append((tg_chat_id, text))


def get_iam_token(oauth_token):
    """Получает временный IAM-токен для работы с API."""
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    response = requests.post(url, json={'yandexPassportOauthToken': oauth_token})
    response.raise_for_status()
    return response.json()['iamToken']


def check_and_start_vm():
    """Проверяет статус ВМ и запускает её при необходимости."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # 1. Авторизация
        iam_token = get_iam_token(OAUTH_TOKEN)
        headers = {'Authorization': f'Bearer {iam_token}'}

        # 2. Получение статуса ВМ
        for instance_id in INSTANCE_IDS:
            get_url = f'https://compute.api.cloud.yandex.net/compute/v1/instances/{instance_id}'
            resp = requests.get(get_url, headers=headers)
            resp.raise_for_status()
            status = resp.json().get('status')

            print(f"[{current_time}] Статус ВМ {instance_id}: {status}")

            # 3. Запуск, если остановлена
            if status in ['STOPPED', 'CRASHED']:
                print(f"[{current_time}] ВМ {instance_id} остановлена. Отправляем команду на запуск...")

                start_url = f'https://compute.api.cloud.yandex.net/compute/v1/instances/{instance_id}:start'
                start_resp = requests.post(start_url, headers=headers)

                if start_resp.status_code == 200:
                    print(f"[{current_time}] Команда на запуск ВМ {instance_id} успешно отправлена!")
                    if USE_TG:
                        msg = f"✅ ВМ `{instance_id}` была остановлена и сейчас **перезапущена** автоматически."
                        send_telegram_message(msg)
                else:
                    print(f"[{current_time}] Ошибка запуска ВМ {instance_id}: {start_resp.text}")
                    if USE_TG:
                        msg = f"⛔ ВМ `{instance_id}` была остановлена. Перезапустить ВМ не удалось."
                        send_telegram_message(msg)
            elif status != "RUNNING":
                if USE_TG:
                    msg = f"⚠️ ВМ `{instance_id}` имеет статус {status}."
                    send_telegram_message(msg)

    except requests.exceptions.RequestException as e:
        print(f"[{current_time}] Ошибка при обращении к API: {e}")
    except Exception as e:
        print(f"[{current_time}] Непредвиденная ошибка: {e}")


if __name__ == '__main__':
    print("Программа мониторинга ВМ запущена...")
    time.sleep(START_TIMEOUT)
    while True:
        check_and_start_vm()
        push_telegram_messages()
        time.sleep(CHECK_INTERVAL_SECONDS)
