
# Перенаправляем выход в лог-файл
exec > >(tee -a alembic.log) 2>&1

echo "Начало процесса миграции..."

# Перемещаемся в корневую директорию проекта
cd $(dirname "$0")/.. || exit

# Настраиваем переменные окружения
export ALEMBIC_CONFIG=./alembic.ini
export DATABASE_URL=$(grep ^DATABASE_URL=.env | cut -d '=' -f2)

# Генерируем миграцию
alembic revision --autogenerate -m "$1"

# Применяем миграцию
alembic upgrade head

echo "Процесс миграции успешно завершен."