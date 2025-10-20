# Task Manager Pro


## 🟢 Описание проекта
Проект представляет собой веб-приложение, построенное на фреймворке FastAPI, которое реализует управление задачами, интеграцию с внешним сервисом календаря и поддержку аутентификации пользователей с использованием JWT. Цель проекта — предоставление удобного инструмента для управления задачами, делегирования их другим пользователям и отслеживания прогресса.

### Основные функции

- **Простое управление задачами:** Создание, изменение и назначение задач сотрудникам.

- **Умные уведомления:** Email-уведомления о назначении новых задач.

- **Отчётность и аналитика:** Полезные отчёты по нагрузке сотрудников и выполненным задачам.

- **Интеграции:** Совместимая работа с Google Calendar



## 🟢 Технологии

Проект использует следующие технологии:

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** Sqlite
- **Authentication:** Passlib, bcrypt
- **Тестирование:** Pytest & Gauge
- **CI/CD:** GitHub Actions
- **Containerization:** Docker
- **API Documentation:** SwaggerUI
- **Data Analysis & Visualization:** Pandas, Plotly



## 🟢 Установка

### Просто выполните следующие шаги:

### Конфигурация Google Calendar API

1. Зарегистрируйте приложение в Google Cloud Console и получите файл `credentials.json`.
2. Создайте копию файла `credentials.example.json` и переименуйте его в `credentials.json`.
3. Поместите его в папку src/app/integretions

### В файле .env заменить данные
- EMAIL_USER=EMAIL_USER
- EMAIL_PASSWORD=EMAIL_PASSWORD



1. **Клонируйте репозиторий**
```shell
git clone https://github.com/lamauspex/Task_Manager
   cd task-manager
   ```


2. **Создание токена**
```shell
mkdir certs
```
```shell
cd certs
```
```shell
openssl genrsa -out jwt-private.pem 2048
```
```shell
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```


3. **Выполните установку**
```shell
pip install -r requirements.txt
```

4. **Запустите приложение**
```shell
uvicorn src.main:app --reload
```

5. **Затем откройте браузер и перейдите по адресу**
```shell
http://localhost:8000
```

6. **Для запуска тестов**
```shell
pytest --html=report.html
```




Ваш вклад в проект приветствуется! Если вы хотите внести изменения или улучшения, создайте pull request или откройте issue на GitHub.

#### Контакты
Если у вас есть вопросы или предложения, не стесняйтесь связаться со мной:

- Имя: Резник Кирилл
- Email: lamauspex@yandex.ru
- GitHub: https://github.com/lamauspex
- Telegram: @lamauspex

Спасибо за интерес к проекту! Надеюсь, он будет полезен в вашей работе.


