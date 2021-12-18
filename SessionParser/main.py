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
DEBUG_ONE_DAY = False
DEBUG_DB = False


def config_logging():
    log_formatter = logging.Formatter("%(asctime)s|%(levelname)5s| %(message)s")
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
    # logging.debug(f"gcl={gcl}")
    # logging.debug(f"gcp={gcp}")
    logging.debug(f"environment={environment}")
    env = (gcl, gcp, environment)
    return env


class CurDate:
    def __init__(self, cur_date_):
        self.cur_date = cur_date_
        self.cur_date_txt = self.cur_date.strftime("%d.%m.%Y")

    def __str__(self):
        return self.cur_date_txt

    def add_day(self):
        self.cur_date = self.cur_date + datetime.timedelta(days=1)
        self.cur_date_txt = self.cur_date.strftime("%d.%m.%Y")


if __name__ == '__main__':
    mine_time = datetime.datetime.now()
    # Конфигурируем формат логирования
    config_logging()
    logging.info('SessionParser start\n')

    # Получаем значения переменных с приватными данными
    logging.info('Настраиваем программу')
    env = get_env()

    # Считываем настройки программы из settings.json
    settings_file = f"settings.{env[2]}.json"
    settings = utils.read_json_file(settings_file)
    try:
        if settings is None:
            raise ValueError("Не удалось получить настройки программы")
    except ValueError as err:
        error_handler(str(err), do_exit=True)
    logging.info('Настройка программы завершена\n')

    # Инициализация БД
    logging.info('Инициализация БД')
    if os.path.isfile(settings['db_file']):
        logging.info(f"База данных {settings['db_file']} обнаружена")
    else:
        logging.error(f"База данных {settings['db_file']} не обнаружена")
        # TODO Сейчас без БД падать не нужно, а далее база должна быть и при её отсутствии нужно падать
        # exit(0)
        database.init_database()
    logging.info('Инициализация БД завершена\n')

    # Соединяемся с БД
    db = database.create_connection(settings['db_file'])
    logging.info(f"Успешное подключение к {settings['db_file']}\n")

    with db:
        # Определить с какой даты начать обработку данных
        logging.info(f"Определяем последнюю обработанную дату")
        # Для отладки берётся один день не из БД
        if DEBUG_ONE_DAY:
            last_date = datetime.datetime.strptime('19.11.2019', "%d.%m.%Y").date()
            end_date = last_date + datetime.timedelta(days=1)
        else:
            last_date = database.select_one(db, r"select value from last_date")[0]
            last_date = datetime.datetime.strptime(last_date, "%d.%m.%Y").date()
            # Конечная дата (по умолчанию это сегодня). Но само сегодня обрабатывать не нужно, т.к. день еще не закончился.
            end_date = datetime.date.today() - datetime.timedelta(days=1)
        # Вычисляем дату с которой начнётся обработка
        cur_date = CurDate(last_date + datetime.timedelta(days=1))
        logging.info(
            f"Последняя обработанная дата (last_date): {last_date.strftime('%d.%m.%Y')} начинаем обработку с: {cur_date}")
        logging.info(f"Дата окончания обработки (end_date): {end_date.strftime('%d.%m.%Y')}\n")

        logging.info('Начинаем обработку данных\n')
        if not DEBUG_DB:
            dict_cache = {}  # Кэш обрабатываемых пользователей в памяти
            browser = parser.init_webdriver(settings)
            parser.login_to_getcourse(browser, env)
        i = 1
        while cur_date.cur_date <= end_date:
            logging.info(f'Обрабатывается день {i}')
            start_time = datetime.datetime.now()
            # Подключаться на сайт и получать данные
            if not DEBUG_DB:
                raw_data = parser.parse_sessions_one_day(settings, env, dict_cache, browser,
                                                         filter_date=cur_date.cur_date_txt)
            # Вносим полученные данные в БД
            if DEBUG_DB:
                # Для отладки берём данные из data_set.py
                import data_set

                raw_data = data_set.data_set

            database.fill_sessions_table(db, raw_data, cur_date.cur_date_txt)

            logging.info(f"===> Обработан {i} день {cur_date.cur_date_txt} "
                         f"за {datetime.datetime.now() - start_time} сек.\n")
            cur_date.add_day()
            i = i + 1

    logging.info(f"Программа завершена")
    logging.info(f"Всего затрачено времени: {datetime.datetime.now() - mine_time} сек.")
