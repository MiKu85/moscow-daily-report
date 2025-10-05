## Moscow Daily Telegram Report Bot

Ежедневный отчёт в Telegram в 08:00 по Москве: погода (Москва), курсы валют (USD/EUR к RUB) и криптовалюты (BTC/ETH/SOL в USD). Работает без сервера — через GitHub Actions.

### Как это работает
- Скрипт `daily_report.py` собирает данные из публичных API и отправляет сообщение в ваш Telegram чат.
- GitHub Actions (`.github/workflows/daily.yml`) запускает скрипт по расписанию ежедневно в 05:00 UTC (08:00 MSK).

### Источники данных
- Погода: Open‑Meteo (Москва)
- Валюты: ЦБ РФ (`cbr-xml-daily.ru`)
- Крипто: CoinGecko (цены в USD)

### Настройка
1. Создайте бота у `@BotFather` и получите токен `BOT_TOKEN`.
2. Узнайте свой `CHAT_ID` у `@userinfobot`.
3. В репозитории GitHub добавьте Secrets: `BOT_TOKEN`, `CHAT_ID` (Settings → Secrets and variables → Actions).
4. Убедитесь, что файлы присутствуют:
   - `requirements.txt`
   - `daily_report.py`
   - `.github/workflows/daily.yml`

### Локальный запуск
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export BOT_TOKEN=xxx CHAT_ID=yyy
python daily_report.py
```

### Ручной запуск из GitHub Actions
Вкладка Actions → Workflow "Daily report 08:00 MSK" → Run workflow.

### Формат сообщения
- Заголовок и дата с эмодзи
- Блок погоды для Москвы
- Курсы USD/EUR к рублю
- Крипто (BTC/ETH/SOL) в USD

### Изменения под себя
- Время (cron) правится в `.github/workflows/daily.yml`.
- Город/координаты — в `fetch_weather_moscow()`.
- Валюты и монеты — в `fetch_fx()` и `fetch_crypto()`.

### Безопасность
- Никогда не коммитьте токены в репозиторий. Используйте Secrets.


