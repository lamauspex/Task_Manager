# Task Manager Pro

> Система управления задачами с аутентификацией JWT, интеграцией с Google Calendar и аналитикой

![FastAPI](https://img.shields.io/badge/FastAPI-0.121-blue?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat&logo=docker)
![Celery](https://img.shields.io/badge/Celery-Redis-green?style=flat)
![JWT](https://img.shields.io/badge/JWT-Auth-orange)

## 🟢 Технологический стек

| Компонент | Технология | Назначение |
|-----------|------------|------------|
| API | FastAPI | HTTP-сервер |
| База данных | PostgreSQL / SQLite | Хранение данных |
| ORM | SQLAlchemy | Работа с БД |
| Аутентификация | JWT + Passlib | Безопасный вход |
| Фоновые задачи | Celery + Redis | Асинхронная обработка |
| Email | SMTP | Уведомления |
| Аналитика | Pandas + Plotly | Визуализация данных |
| Интеграции | Google Calendar API | Синхронизация календаря |
| Тестирование | Pytest | Unit-тесты |
| Docker | Docker Compose | Контейнеризация |

## 🟢 Ключевые навыки

- **FastAPI** — асинхронный REST API
- **JWT-аутентификация** — безопасность
- **Google Calendar API** — интеграция с календарём
- **Celery + Redis** — фоновые задачи
- **Email-уведомления** — SMTP
- **Аналитика** — Pandas + Plotly визуализация
- **Docker** — контейнеризация

## 🟢 Возможности

- Создание, изменение и удаление задач
- Делегирование задач сотрудникам
- Email-уведомления о новых задачах
- Интеграция с Google Calendar
- Аналитика и отчёты по нагрузке
- Визуализация данных (графики)
- JWT-аутентификация
- Docker-развёртывание

## 🟢 Структура проекта

```
├── app.py                      # Точка входа
├── certs/                      # JWT ключи
├── src/
│   └── app/
│       ├── routers/            # API эндпоинты
│       ├── models/             # SQLAlchemy модели
│       ├── schemas/            # Pydantic схемы
│       ├── core/               # Конфигурация, БД, Celery
│       ├── integrations/       # Google Calendar
│       ├── analytics/          # Аналитика и графики
│       ├── services/           # Бизнес-логика
│       └── middlewares/        # Middleware
├── infra/                      # Docker
├── scripts/                    # Скрипты
├── tests/                      # Тесты
└── requirements.txt
```

## 🟢 Быстрый старт


### Клонирование
```bash
git clone https://github.com/lamauspex/Task_Manager.git
```
```bash
cd Task_Manager
```
### Установка зависимостей
```bash
pip install -r requirements.txt
```
### Запуск
```bash
uvicorn app:app --reload
```

Откройте http://localhost:8000

## 🟢 Docker

### Раскомментируйте DATABASE_URL в .env для PostgreSQL
```bash
docker-compose -f infra/docker/docker-compose.yml up -d
```

## 🟢 Основные endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/auth/register` | Регистрация |
| `POST` | `/auth/login` | Вход |
| `GET` | `/tasks/` | Список задач |
| `POST` | `/tasks/` | Создание задачи |
| `PUT` | `/tasks/{id}/` | Обновление задачи |
| `DELETE` | `/tasks/{id}/` | Удаление задачи |
| `GET` | `/analytics/load` | Аналитика нагрузки |

## 🟢 Архитектура

```
┌─────────────────────────────────────────────┐
│              FastAPI (REST API)             │
├─────────────────────────────────────────────┤
│  Auth  │  Tasks  │  Analytics  │  Calendar  │
├─────────────────────────────────────────────┤
│        Celery (async tasks)  │  Redis       │
├─────────────────────────────────────────────┤
│          PostgreSQL / SQLite                │
└─────────────────────────────────────────────┘
```

---

**Автор**: Резник Кирилл  
**Email**: lamauspex@yandex.ru  
**Telegram**: @lamauspex  
**GitHub**: https://github.com/lamauspex




