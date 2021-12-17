#!/usr/bin/env python

import logging
import os
import database
import utils
import parser
import datetime
from error_handling import error_handler as error_handler

# Global variables
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
    gcl = os.getenv('GCL')
    gcp = os.getenv('GCP')
    # Определяет среду в которой выполняется программа dev, prod и т.п. Для каждой среды свои настройки.
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
    env = (gcl, gcp, environment)
    return env


if __name__ == '__main__':
    # Конфигурируем формат логирования
    config_logging()
    logging.info('SessionParser start')

    # Получаем значения переменных с приватными данными
    env = get_env()

    # Считываем настройки программы из settings.json
    settings_file = f"settings.{env[2]}.json"
    settings = utils.read_json_file(settings_file)
    try:
        if settings is None:
            raise ValueError("Не удалось получить настройки программы")
    except ValueError as err:
        error_handler(str(err), do_exit=True)

    # Инициализация БД
    if os.path.isfile(settings['db_file']):
        logging.info(f"База данных {settings['db_file']} обнаружена")
    else:
        logging.error(f"База данных {settings['db_file']} не обнаружена")
        # TODO Сейчас без БД падать не нужно, а далее база должна быть и при её отсутствии нужно падать
        # exit(0)
        database.init_database()

    # Соединяемся с БД
    db = database.create_connection(settings['db_file'])
    logging.info(f"Успешное подключение к {settings['db_file']}")
    with db:
        # Определить с какой даты начать обработку данных
        logging.info(f"Определяем последнюю обработанную дату")

        # TODO пока для отладки дату не из БД беру а прямо здесь
        # last_date = database.select_one(db, r"select value from last_date")[0]
        last_date = '19.11.2019'

        date_parts = last_date.split('.')
        next_date = (datetime.datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])) +
                     datetime.timedelta(days=1)).strftime("%d.%m.%Y")
        logging.info(f"Найдена последняя обработанная дата: {last_date} начинаем обработку с: {next_date}")

        # Подключаться на сайт и получать данные
        dict_cache = {}  # Кэш обрабатываемых пользователей в памяти
        browser = parser.init_webdriver(settings)
        parser.login_to_getcourse(browser, env)
        parser.parse_sessions_one_day(settings, env, dict_cache, browser, filter_date=next_date)
