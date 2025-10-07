# Используем минималистичный образ Python
FROM python:3.11-slim

# Определяем рабочую директорию
WORKDIR /code

# Копируем только файл requirements.txt, чтобы ускорить кэширование слоев
COPY ./requirements.txt /code/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY . /code/

# Проставляем права для файлов (при необходимости)
RUN chmod +x scripts/*.sh

# Экспортируем переменные окружения из .env файла
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Устанавливаем точку входа
ENTRYPOINT ["python", "-m", "src.main"]