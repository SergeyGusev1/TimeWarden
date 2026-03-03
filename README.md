# TimeWarden ⏱️
[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.129-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Pet-проект** — асинхронный трекер времени, который автоматически определяет, на что вы тратите время за компьютером. Проект находится в активной разработке.

## 🚀 **О проекте**

TimeWarden состоит из двух частей:
- **Сервер** (FastAPI + SQLAlchemy) — принимает данные, категоризирует активность, отдаёт статистику
- **Агент** (клиент на Python) — работает в фоне, собирает информацию об активных окнах и отправляет на сервер

## 🛠️ **Стек технологий**

- **FastAPI** — асинхронный веб-фреймворк
- **SQLAlchemy 2.0** — асинхронная ORM
- **Alembic** — миграции базы данных
- **SQLite + aiosqlite** — база данных для разработки
- **Pydantic** — валидация данных
- **psutil + ctypes** — сбор информации о процессах (агент)

## 📦 **Установка и запуск**

### Сервер

```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/TimeWarden.git
cd TimeWarden
```

### Быстрый старт
```bash
# Клонировать репозиторий
git clone https://github.com/SergeyGusev1/TimeWarden.git
cd TimeWarden
```
```bash
# Создать .env файл
cp .env.example .env
# Отредактировать .env (добавить токены Telegram)
```
```bash
# Запустить все сервисы
docker-compose up --build
```
# Сервисы будут доступны:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000/docs
# - PostgreSQL: localhost:5432

# Агент
```bash
# В отдельной папке или терминале
cd agent  # или отдельный репозиторий

# Установить зависимости
pip install requirements.txt

# Запустить агента
python agent.py
```

📁 Структура проекта
```bash
TimeWarden/
├── backend/                    # Весь бэкенд
│   ├── app/                    # FastAPI приложение
│   │   ├── api/
│   │   ├── core/
│   │   ├── crud/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/                # Миграции
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # Весь фронтенд
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
│
├── agent/                      # Агент
│   └── collector.py
│
├── .gitignore
├── README.md
└── docker-compose.yml
```
# 🎯 Функциональность

Уже работает ✅
✅ Сбор информации об активном окне (Windows)

✅ Автоматическая категоризация приложений (productive/neutral/wasteful)

✅ Отправка данных на сервер

✅ Сохранение в БД

✅ API с пагинацией

✅ Асинхронная обработка запросов

# В разработке 🚧
🚧 Статистика и графики

🚧 Веб-интерфейс

🚧 Авторизация пользователей

🚧 Экспорт данных

🚧 Настройка правил категоризации

🚧 Поддержка Linux/macOS для агента

# 📊 Пример API
```bash
http
POST /api/v1/activities
{
    "app_name": "chrome.exe",
    "window_title": "YouTube - Google Chrome",
    "duration_seconds": 120.5,
    "start_time": "2024-01-01T10:00:00",
    "end_time": "2024-01-01T10:02:00"
}

GET /api/v1/activities?page=1&size=10
{
    "items": [...],
    "total": 42,
    "page": 1,
    "size": 10
}
```
# 🐍 Агент
Агент работает в фоне и собирает данные:

Каждые 5 секунд проверяет активное окно

При смене окна записывает длительность

Раз в 30 секунд отправляет накопленные данные на сервер

При ошибках сохраняет данные в буфере

## 🤖 **Telegram-бот**

TimeWarden может присылать уведомления в Telegram:

### Настройка
1. Напиши @BotFather в Telegram, создай нового бота
2. Получи токен и добавь в `.env`:
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
3. Найди @getmyid_bot, чтобы узнать свой chat_id

### Что умеет бот
- 📊 Ежедневный отчёт в 21:00
- ⚠️ Предупреждения о чрезмерном wasted-времени
- 🎉 Поздравления с достижением целей


# 🤝 Вклад в проект
Проект создан в образовательных целях и для портфолио. Любые идеи и предложения приветствуются!


Статус: В активной разработке 🚧


## 🎯 **Что получилось:**
- Чёткое описание проекта
- Упоминание что в разработке 🚧
- Инструкции по установке
- Список готового и планируемого
- Примеры API
