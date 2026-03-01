# API Reference

Подробные примеры запросов к API.

## Аутентификация

### Регистрация пользователя

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secret123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Вход в систему

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secret123"
  }'
```

Ответ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## Задачи

### Создание задачи

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Новая задача",
    "description": "Описание задачи",
    "priority": "high",
    "deadline": "2025-12-31T23:59:00"
  }'
```

### Получение списка задач

```bash
curl -X GET http://localhost:8000/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Получение задачи по ID

```bash
curl -X GET http://localhost:8000/tasks/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Обновление задачи

```bash
curl -X PUT http://localhost:8000/tasks/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Обновлённая задача",
    "description": "Новое описание",
    "status": "in_progress"
  }'
```

### Удаление задачи

```bash
curl -X DELETE http://localhost:8000/tasks/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Пользователи

### Получение профиля

```bash
curl -X GET http://localhost:8000/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Обновление профиля

```bash
curl -X PUT http://localhost:8000/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith"
  }'
```

---

## Аналитика

### Нагрузка сотрудников

```bash
curl -X GET http://localhost:8000/analytics/load \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Статистика задач

```bash
curl -X GET http://localhost:8000/analytics/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Google Calendar

### Синхронизация задачи с календарём

```bash
curl -X POST http://localhost:8000/tasks/1/sync-calendar \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Notes

- Во всех запросах, требующих авторизации, добавляйте заголовок `Authorization: Bearer YOUR_TOKEN`
- Токен получаете после успешного `/auth/login`
- Срок действия токена: настраивается в `.env` (по умолчанию 30 минут)
