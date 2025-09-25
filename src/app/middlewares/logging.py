
""" Назначение: Настройки логирования """


import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


class LoggingSettings:
    """
    Настройка стандартного механизма логирования
     LOG_DIR: Директория для хранения логов
     MAX_BYTES: Максимальный размер файла перед ротацией
     BACKUP_COUNT: Количество сохраняемых резервных копий
    """

    LOG_DIR: str = './logs'
    MAX_BYTES: int = 10 * 1024 * 1024
    BACKUP_COUNT: int = 5

    @classmethod
    def setup_logging(cls):

        # Создаем директорию, если её ещё нет
        Path(cls.LOG_DIR).mkdir(parents=True, exist_ok=True)
        # Имя файла лога
        log_file_path = Path(cls.LOG_DIR) / 'app.log'

        # Получаем глобального лоогера
        logger = logging.getLogger('task_manager')
        logger.setLevel(logging.DEBUG)

        # Форматировщик для записи в файл
        file_formatter = logging.Formatter(
            '%(asctime)s - '
            '%(name)s - '
            '%(levelname)s - '
            '%(pathname)s:%(lineno)d - '
            '%(message)s'
        )

        # Форматировщик для терминала
        terminal_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s]: %(message)s')

        # Ротация файлов
        rotating_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=cls.MAX_BYTES,
            backupCount=cls.BACKUP_COUNT
        )
        rotating_handler.setFormatter(file_formatter)

        # Вывод в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(terminal_formatter)
        console_handler.setLevel(logging.INFO)

        # Добавляем обработчики
        logger.addHandler(rotating_handler)
        logger.addHandler(console_handler)

        return logger
