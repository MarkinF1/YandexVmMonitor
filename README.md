# ☁️ Yandex Cloud VM Autorestarter

Python-скрипт для автоматического мониторинга и перезапуска **прерываемых (preemptible)** виртуальных машин в Yandex Cloud. 

Если облако останавливает вашу машину из-за нехватки ресурсов или истечения 24-часового лимита, скрипт обнаружит это, отправит команду на запуск и пришлет уведомление в Telegram.

## 🚀 Возможности

* **Мониторинг 24/7**: Постоянная проверка статуса ваших ВМ через API.
* **Автозапуск**: Автоматический ввод машины в строй при обнаружении статусов `STOPPED` или `CRASHED`.
* **Уведомления**: Настройка оповещений в Telegram для одного или нескольких пользователей.
* **Кэширование токенов**: Экономное использование ресурсов API (обновление IAM-токена раз в час).

---

## 🛠 Настройка

Все параметры конфигурации хранятся в файле `config.py`.

> [!IMPORTANT]
> **Безопасность:** Если вы планируете сделать свой репозиторий публичным, обязательно добавьте `config.py` в файл `.gitignore`, чтобы ваши секретные токены не попали в открытый доступ.

### 1. Данные Yandex Cloud
* **OAUTH_TOKEN**: Получите его, перейдя по **[этой ссылке](https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb)**.
* **INSTANCE_IDS**: Скопируйте «Идентификатор» вашей ВМ в консоли Yandex Cloud (раздел «Обзор», формат `fhm8...`). Можно указать несколько ID списком.

### 2. Настройка Telegram (опционально)
1.  **TG_TOKEN**: Создайте бота через **[@BotFather](https://t.me/BotFather)** (команда `/newbot`).
2.  **TG_CHAT_IDS**: Узнайте свой ID через бота **[@userinfobot](https://t.me/userinfobot)**.
3.  **Активация**: Обязательно нажмите **"Запустить" (Start)** в вашем боте, иначе он не сможет отправлять вам сообщения.

---

## 📦 Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone git@github.com:MarkinF1/YandexVmMonitor.git
    cd YandexVmMonitor
    ```

2.  **Установите зависимости:**
    ```bash
    pip install requests
    ```

3.  **Заполните `config.py`** своими данными.

4.  **Запустите мониторинг:**
    ```bash
    python main.py
    ```

---

## 🔄 Работа в фоновом режиме (systemd)

Для надежной работы на Linux-сервере рекомендуется создать системную службу, которая будет запускать скрипт автоматически.

1.  **Создайте файл сервиса:**
    ```bash
    sudo nano /etc/systemd/system/yc-monitor.service
    ```

2.  **Вставьте содержимое** (заменив `/path/to/your/folder` на реальный путь):
    ```ini
    [Unit]
    Description=Yandex Cloud VM Monitor
    After=network.target

    [Service]
    Type=simple
    User=root
    WorkingDirectory=/path/to/your/folder
    ExecStart=/usr/bin/python3 main.py
    Restart=always
    RestartSec=10

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Активируйте службу:**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable yc-monitor
    sudo systemctl start yc-monitor
    ```

## 📄 Лицензия
Этот проект распространяется под лицензией MIT.