import os
from typing import List


# Данные Яндекс Облака
OAUTH_TOKEN: str = os.getenv('OAUTH_TOKEN', 'ВАШ_OAUTH_ТОКЕН')
instance_ids: str = os.getenv('INSTANCE_IDS', ['ID_ВАШЕЙ_ВИРТУАЛЬНОЙ_МАШИНЫ'])
INSTANCE_IDS: List[str] = [instance_id.strip() for instance_id in instance_ids.split(",") if instance_id.strip()]
START_TIMEOUT: int = int(os.getenv('START_TIMEOUT', 10)) # Интервал для таймаута при старте
CHECK_INTERVAL_SECONDS: int = int(os.getenv('CHECK_INTERVAL_SECONDS', 60))  # Интервал проверки (в секундах)

# Данные Telegram
USE_TG: bool = os.getenv('USE_TG', "false").lower() in ("true", "1", "yes") # Если True, то отправляем в тг, если False - нет
TG_TOKEN: str = os.getenv('TG_TOKEN', 'Токен вашего телеграм бота')
tg_chat_ids: str = os.getenv('TG_CHAT_IDS', 'Аккаунты телеграмма для отправки сообщений')
TG_CHAT_IDS: List[str] = [tg_chat_id.strip() for tg_chat_id in tg_chat_ids.split(",") if tg_chat_id.strip()]
