import os
from dotenv import load_dotenv


def config():
    """Загружает переменные окружения из файла .env и возвращает их в виде словаря."""
    load_dotenv()

    db_params = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }

    if any(value is None for value in db_params.values()):
        raise Exception("Не все переменные окружения для подключения к БД определены в .env файле.")

    return db_params