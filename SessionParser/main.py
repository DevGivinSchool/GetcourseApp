#!/usr/bin/env python

import logging
import os
import traceback
import database
from error_handling import error_handler as error_handler

DEBUG = True


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
    GCL: str | None = os.getenv('gcl')
    GCP: str | None = os.getenv('gcp')
    try:
        if GCL is None:
            raise EnvironmentError("Не определена переменная GCL")
        if GCP is None:
            raise EnvironmentError("Не определена переменная GPL")
    except EnvironmentError as err:
        error_handler(str(err), do_exit=True)
    logging.debug(GCL)
    logging.debug(GCP)


if __name__ == '__main__':
    # Конфигурируем формат логирования
    config_logging()
    logging.info('SessionParser start')
    # Получаем значения переменных с приватными данными
    get_env()
    # TODO Инициализация БД
    if os.path.isfile('sp.db'):
        logging.info('База данных sp.db обнаружена')
    else:
        logging.error('База данных sp.db не обнаружена')
        # TODO Сейчас без БД падать не нужно, а далее база должна быть
        # exit(0)
        database.init_database()

    db = database.create_connection('sp.db')
    