# Usage Guide

## Руководство пользователя предназначено для ознакомления с возможностями нашего API и рекомендациями по правильному использованию.

### Getting Started

Перед началом работы убедитесь, что ваш проект установлен и запущен. Следуйте простым шагам:

#### Конфигурация Google Calendar API

1. Зарегистрируйте приложение в Google Cloud Console и получите файл `credentials.json`.
2. Создайте копию файла `credentials.example.json` и переименуйте его в `credentials.json`.
3. Поместите его в папку src/app/integretions

#### В файле .env заменить данные
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



### Endpoints Reference
Ниже приведены основные конечные точки (routes) нашего API с примерами запросов.

#### Users Endpoints
POST /users: Создает нового пользователя.curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"secret"}'

GET /users/:id: Получает информацию о пользователе по его уникальному идентификатору.curl -X GET http://localhost:8000/users/1

PUT /users/:id: Обновляет информацию о пользователе.curl -X PUT http://localhost:8000/users/1 -H "Content-Type: application/json" -d '{"firstName":"John","lastName":"Doe"}'


#### Tasks Endpoints
POST /tasks: Создает новую задачу.curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"New Task","description":"This is a new task."}'

GET /tasks/:id: Получает информацию о задаче по её идентификатору.curl -X GET http://localhost:8000/tasks/1

PUT /tasks/:id: Обновляет задачу.curl -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d '{"title":"Updated Title","description":"Updated Description"}'



### Authentication
Аутентификация выполняется с использованием JWT (JSON Web Tokens). Токен необходим для большинства маршрутов, требующих авторизацию.

Login: Выполняя запрос на /login, вы получаете JWT-токен, который необходимо передавать в последующих запросах.


### Testing
Вы можете воспользоваться встроенными средствами тестирования FastAPI для написания и запуска тестов:

pytest tests


### Conclusion
Это руководство охватывает основы использования нашего API и даёт представление о возможных операциях с данными. Продолжайте изучать документацию и экспериментируйте с нашим API для лучшего понимания возможностей.