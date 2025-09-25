# Task Manager Pro


## 🟢 Описание проекта
Система управления задачами для компаний любого масштаба.
Повышает эффективность бизнеса путём удобной организации задач,
контроля сроков и поддержки командной работы.

### Основные функции

- **Простое управление задачами:** Создание, изменение и назначение задач сотрудникам.

- **Интерактивный календарь:** Графический календарь с дедлайнами и прогрессом выполнения.

- **Умные уведомления:** Email-уведомления о событиях и изменениях.

- **Отчётность и аналитика:** Полезные отчёты по нагрузке сотрудников и выполненным задачам.

- **Интеграции:** Совместимая работа с Google Calendar, Slack и Trello.



## 🟢 Технологии

Проект использует следующие технологии:

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** Sqlite
- **Authentication:** Passlib, bcrypt
- **Тестирование:** Pytest & Gauge
- **CI/CD:** GitHub Actions
- **Containerization:** Docker & Docker Compose
- **API Documentation:** SwaggerUI
- **Data Analysis & Visualization:** Pandas, Plotly



## 🟢 Установка

### Просто выполните следующие шаги:


1. **Клонируйте репозиторий**
```shell
git clone https://github.com/lamauspex/Task_Manager
   cd task-manager
   ```


2. **Создание токена**
   ```shell
  mkdir certs
  cd certs
  openssl genrsa -out jwt-private.pem 2048
  openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
  ```

3. **Выполните установку**
   ```shell
   pip install -r requirements.txt
   ```

4. **Затем откройте браузер и перейдите по адресу**
   ```
   http://localhost:8000
   ```

```

Ваш вклад в проект приветствуется! Если вы хотите внести изменения или улучшения, создайте pull request или откройте issue на GitHub.

**Контакты**
Если у вас есть вопросы или предложения, не стесняйтесь связаться со мной:

Имя: Резник Кирилл
Email: lamauspex@yandex.ru
GitHub: https://github.com/lamauspex
Telegram: @lamauspex

Спасибо за интерес к проекту! Надеюсь, он будет полезен в вашей работе.


