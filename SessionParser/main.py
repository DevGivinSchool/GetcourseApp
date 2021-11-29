#!/usr/bin/env python

import logging
import os
import traceback
import sys


def config_logging():
    log_formatter = logging.Formatter("%(asctime)s|%(levelname)8s| %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(log_formatter)
    custom_logger = logging.getLogger("")
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(handler)


def error_handling(message, do_exit=False):
    error_text = f"ERROR: {message}\n{traceback.format_exc()}"
    logging.error(error_text)
    if do_exit:
        sys.exit(f"Программа завершилась ошибкой\n{error_text}")


def get_env():
    logging.info('Get environment variables')
    GCL: str | None = os.getenv('gcl')
    GCP: str | None = os.getenv('gcp')
    try:
        if GCL is None:
            raise EnvironmentError("Не определена переменная GCL")
        if GPL is None:
            raise EnvironmentError("Не определена переменная GPL")
    except EnvironmentError as err:
        error_handling(str(err), do_exit=True)
    logging.debug(GCL)
    logging.debug(GCP)


if __name__ == '__main__':
    # Конфигурируем формат логирования
    config_logging()
    logging.info('SessionParser start')
    # Получаем значения переменных с приватными данными
    get_env()
    # TODO Инициализация БД
