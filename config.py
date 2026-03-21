# Данные Яндекс Облака
OAUTH_TOKEN = 'ВАШ_OAUTH_ТОКЕН'
INSTANCE_IDS = ['ID_ВАШЕЙ_ВИРТУАЛЬНОЙ_МАШИНЫ']
START_TIMEOUT = 10 # Интервал для таймаута при старте
CHECK_INTERVAL_SECONDS = 60  # Интервал проверки (в секундах)

# Данные Telegram
USE_TG = False # Если True, то отправляем в тг, если False - нет
TG_TOKEN = 'Токен вашего телеграм бота'
TG_CHAT_IDS = ['Аккаунты телеграмма для отправки сообщений']

# Данные прокси
USE_PROXY = False  # Установите True, чтобы включить прокси
PROXY_URL = 'http://user:password@host:port' # Пример: 'http://127.0.0.1:8080'