# Manas AI Assistant 🤖

Telegram-бот для абитуриентов Кыргызско-Турецкого университета «Манас» (КТУМ). Отвечает на вопросы о поступлении, экзаменах и университете с помощью **Google Gemini 2.0 Flash**.

## Возможности

- 🏛 **Информация об университете** — ответы на вопросы на основе данных КТУМ
- 📖 **Гуманитарные науки** — Кыргызский язык, Литература, История, География
- 🔬 **Естественные науки** — Математика, Физика, Биология, Химия
- 💡 **Интеграция с Gemini AI** — генерация ответов с контекстным пониманием

## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/manas-ai-assistant.git
   cd manas-ai-assistant
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте Telegram бота через [@BotFather](https://t.me/BotFather) и получите API ключ Gemini от [Google AI Studio](https://aistudio.google.com/).

4. Настройте переменные окружения:
   ```bash
   cp .env.example .env
   # Отредактируйте .env, вставьте свои ключи
   ```

5. Запустите бота:
   ```bash
   python main.py
   ```

## Docker

```bash
docker build -t manas-ai-assistant .
docker run --env-file .env manas-ai-assistant
```

## Deploy на Heroku

Проект содержит `Procfile` для деплоя на Heroku:

```bash
heroku create
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

## Структура

```
├── main.py                    # Основной код бота
├── files/
│   └── university_info.txt    # Данные об университете (контекст)
├── Dockerfile
├── Procfile
├── requirements.txt
└── .env.example
```

## Технологии

- **Python 3.10+**
- **pyTelegramBotAPI** — Telegram Bot API
- **Google Generative AI (Gemini 2.0 Flash)** — генерация ответов
- **python-dotenv** — управление переменными окружения
