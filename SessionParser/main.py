#!/usr/bin/env python

import logging
import os
import database
import utils
from error_handling import error_handler as error_handler

# Global variables
DEBUG = True
gcl = None
gcp = None
environment = None  # Определяет среду в которой выполняется программа dev, prod и т.п. Для каждой среды свои настройки.


def config_logging():
    log_formatter = logging.Formatter("%(asctime)s|%(levelname)8s| %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(log_formatter)
    custom_logger = logging.getLogger("")
    if DEBUG:
        custom_logger.setLevel(logging.DEBUG)
    else:
        custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(handler)


def get_env():
    logging.info('Get environment variables')
    global gcl
    global gcp
    global environment
    gcl = os.getenv('GCL')
    gcp = os.getenv('GCP')
    environment = os.getenv('ENVIRONMENT')
    try:
        if gcl is None:
            raise EnvironmentError("Не определена переменная GCL")
        if gcp is None:
            raise EnvironmentError("Не определена переменная GPL")
        if environment is None:
            raise EnvironmentError("Не определена переменная ENVIRONMENT")
    except EnvironmentError as e:
        error_handler(str(e), do_exit=True)
    logging.debug(f"gcl={gcl}")
    logging.debug(f"gcp={gcp}")
    logging.debug(f"environment={environment}")


if __name__ == '__main__':
    db_file = 'sp.db'  # Путь к БД

    # Конфигурируем формат логирования
    config_logging()
    logging.info('SessionParser start')

    # Получаем значения переменных с приватными данными
    get_env()

    # Считываем настройки программы из settings.json
    settings_file = f"settings.{environment}.json"
    settings = utils.read_json_file(settings_file)
    try:
        if settings is None:
            raise ValueError("Не удалось получить настройки программы")
    except ValueError as err:
        error_handler(str(err), do_exit=True)

    # TODO Инициализация БД
    if os.path.isfile(settings['db_file']):
        logging.info(f'База данных {db_file} обнаружена')
    else:
        logging.error(f'База данных {db_file} не обнаружена')
        # TODO Сейчас без БД падать не нужно, а далее база должна быть и при её отсутствии нужно падать
        # exit(0)
        database.init_database()

    # Соединяемся с БД
    db = database.create_connection(db_file)
    logging.info(f"Успешное подключение к {db_file}")

    # TODO Подключаться на сайт и получать данные
