"""
Модуль конфигурации структурированного JSON логирования.

Настройка логирования для всего приложения.
В debug режиме — читаемый текст, в production — JSON формат.
"""

# Импорты для работы с логированием
import logging
# Импорты для вывода в stdout
import sys
# Импорты для типизации
from typing import Any

# Импорты настроек приложения
from backend.src.app.core.config import settings


class JSONFormatter(logging.Formatter):
    """
    Минимальный структурированный форматтер.

    Выводит логи в формате ключ=значение (JSON).
    Используется в production для удобного парсинга.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Форматирование записи лога в JSON.

        Args:
            record: Запись лога от logging модуля.

        Returns:
            str: JSON строка с данными лога.
        """
        # Импортируем json для сериализации
        import json
        # Словарь для хранения данных лога
        log_data: dict[str, Any] = {
            # Время лога
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,  # Уровень (INFO, ERROR, etc.)
            "logger": record.name,  # Имя логгера
            "message": record.getMessage(),  # Сообщение лога
        }
        # Если есть информация об исключении — добавляем
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        # Сериализуем в JSON (ensure_ascii=False для поддержки кириллицы)
        return json.dumps(log_data, ensure_ascii=False)


def configure_logging() -> None:
    """
    Настройка корневого логгера при старте приложения.

    Вызывается один раз в lifespan приложении.
    Настраивает уровень, форматтер и фильтрует шумные логгеры.
    """
    # Уровень логирования: DEBUG в режиме отладки, INFO в production
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    # Обработчик для вывода в консоль (stdout)
    handler = logging.StreamHandler(sys.stdout)
    # Устанавливаем форматтер: читаемый в debug, JSON в production
    handler.setFormatter(
        logging.Formatter("%(levelname)s  %(name)s  %(message)s")
        if settings.DEBUG
        else JSONFormatter()
    )
    # Базовая настройка logging с нашими параметрами
    logging.basicConfig(
        level=level,  # Уровень логирования
        handlers=[handler],  # Наши обработчики
        force=True,  # Перезаписать существующие настройки
    )
    # Отключаем шумные логгеры третьих сторон
    for noisy in ("sqlalchemy.engine", "uvicorn.access"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


# Глобальный логгер для приложения
logger = logging.getLogger("task_manager")
