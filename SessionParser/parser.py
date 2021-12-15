import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from error_handling import error_handler as error_handler
from typing import List

TIMEOUT = 1  # timeout in sec


def parse_sessions_one_day(settings, env, filter_date: str):
    logging.info(f"Start parse sessions")
    try:
        browser = init_webdriver(settings)

        login_to_getcourse(browser, env)

        # Открыть страницу sessions
        logging.debug("Открыть страницу Трафик - Сессии")
        logging.debug("link=https://givin.school/pl/metrika/traffic/visit-list")
        browser.get("https://givin.school/pl/metrika/traffic/visit-list")
        time.sleep(TIMEOUT)

        filter2_select_dates(browser, filter_date)  # Кнопка "Выбрать даты" и заполнение полей дат
        time.sleep(TIMEOUT)
        filter3_columns(browser)  # Кнопка "Колонки" и чекнуть все колонки
        time.sleep(TIMEOUT)
        filter1_add_conditions(browser)  # Кнопка "Добавить условие" и выбор в меню пункта "Авторизованный"
        time.sleep(TIMEOUT)

        # Здесь кликаю по h1 просто чтобы выйти из поля даты
        # logging.debug("Поиск h1")
        # div_h1 = browser.find_element(By.TAG_NAME, "h1")
        # div_h1.click()
        # time.sleep(10)

        # Поиск кнопки Показать еще. Её нужно кликнуть столько раз чтобы список раскрылся полностью.
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        count_button_show_more, button_show_more = find_button_show_more(browser)
        count_button_show_more2 = 0
        if count_button_show_more > 0:
            # Нажимать кнопку Показать еще до тех пор пока не перестанут появлятся её новые экземпляры
            while count_button_show_more > count_button_show_more2:
                count_button_show_more2 = count_button_show_more
                logging.debug(f"Нажимаю на кнопку - {button_show_more.text}")
                button_show_more.click()
                time.sleep(TIMEOUT)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(TIMEOUT)
                count_button_show_more, button_show_more = find_button_show_more(browser)
        time.sleep(TIMEOUT)

        # Parsing table
        raw_data = get_raw_data_from_table(browser, filter_date)
        # TODO 2) Распарсить контакт (узнать его email + telegram если они есть).
        #         Сходить на страницу пользователя и взять данные оттуда.
        #         Нужно проверять что такой пользователь уже обрабатывался, чтобы не парсить лишнего.
        #         Делать это лучше через кэш в памяти = словарь, а уж потом лезть в БД.
        # TODO 3) Занести даннные в БД (нужно возвращать набор данных, а вышестоящая процедура это делает)
        # TODO 4) Вынести login_to_getcourse и init_webdriver из этой процедуры parse_sessions_one_day

        # Пауза чтобы рассмотреть результат
        time.sleep(30)

        # закрываем браузер после всех манипуляций
        logging.debug("Закрываем браузер после всех манипуляций")
        browser.quit()
    except Exception as e:  # noqa: E722
        error_handler("Ошибка парсинга страницы", do_exit=True)
    finally:
        # закрываем браузер даже в случае ошибки
        # time.sleep(30)
        browser.quit()
    logging.info(f"End parse sessions")


def get_raw_data_from_table(browser, filter_date) -> List[str]:
    logging.debug("Парсинг таблицы")
    table = browser.find_element(By.TAG_NAME, "tbody")
    # html_table_body = table.get_attribute('innerHTML')
    # print(f"html_table_body:\n{html_table_body}")
    table_body = BeautifulSoup(table.get_attribute('innerHTML'))
    raw_data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')  # <class 'bs4.element.ResultSet'>
        if len(cols) != 30:  # Пропуск кнопок "Показать еще", они в этой же таблице
            continue

        href = cols[13].find('a').get('href')  # <class 'bs4.element.Tag'> Получить ссылку на профиль Пользователя
        address = cols[3].text.strip()  # что-то типа 'RU, Калининградская область, Калининград 83.219.136.214'

        cols = [ele.text.strip() for ele in cols]
        cols2 = [ele for ele in cols if ele]  # Пропуск пустых колонок '' (в самом начале иконка)

        cols2.append(href.rsplit("/", 1)[1])  # Добавить столбец ID Пользователя
        cols2.append(href)  # Добавить столбец ссылку на профиль Пользователя
        cols2.extend(get_address(address))  # Добавить country, region, city, ip
        raw_data.append(cols2)
    logging.debug(f"В таблице за {filter_date} всего {len(raw_data)} строк")
    for line in raw_data:
        logging.debug(line)
    return raw_data


def get_address(address_str):
    """
    Преобразовать строку адреса в List[country, region, city, ip].
    Количество адресных элементов в address_str может быть разным!
    :param address_str: 'RU, Калининградская область, Калининград 83.219.136.214'
    :return:
    """
    country = region = city = ip = None
    address_list = address_str.split(", ")
    match len(address_list):
        case 1:  # RU 85.249.173.163
            temp2 = address_list[0].split(" ")
            country = temp2[0]
            region = '-- пусто --'
            city = '-- пусто --'
            ip = temp2[1]
        case 2:  # CY, Лимасол 62.228.31.136
            temp2 = address_list[1].split(" ")
            country = address_list[0]
            region = '-- пусто --'
            city = temp2[0]
            ip = temp2[1]
        case 3:  # RU, Краснодарский край, Сочи 185.15.61.154
            temp2 = address_list[2].split(" ")
            country = address_list[0]
            region = address_list[1]
            city = temp2[0]
            ip = temp2[1]
        case _:
            try:
                raise ValueError(f"В адрес: '{address_str}' нестандартное количество элементов: {len(address_list)}")
            except ValueError as err:
                error_handler(str(err), do_exit=True)
    return [country, region, city, ip]


def find_button_show_more(browser):
    """
    Поиск кнопки Показать еще.
    :param browser:
    :return: Возвращает количество кнопок и самую последнюю из них. Если кнопки нет - 0, None.
    """
    logging.debug("Поиск кнопки Показать еще")
    list_button_show_more = browser.find_elements(By.CSS_SELECTOR, "a.btn.btn-default")
    count_button_show_more = len(list_button_show_more)
    logging.debug(f"Количество кнопок Показать еще - {count_button_show_more}")
    if count_button_show_more == 0:
        button_show_more = None
    else:
        button_show_more = list_button_show_more[-1]
        logging.debug(f"Кнопка Показать еще - {button_show_more.text}")
    return count_button_show_more, button_show_more


def filter2_select_dates(browser, filter_date):
    # Поиск кнопки Выбрать даты и заполнение полей дат
    logging.debug("Поиск кнопки Выбрать даты")
    button_select_dates = browser.find_element(By.CSS_SELECTOR, "span#select2-chosen-4.select2-chosen")
    button_select_dates.click()
    logging.debug("Поиск поля ввода и выбор пункта Выбрать даты")
    search_input = browser.find_element(By.CSS_SELECTOR, "input#s2id_autogen4_search.select2-input")
    search_input.clear()
    search_input.send_keys("Выбрать даты")  # Выбрать даты
    search_input.send_keys(Keys.RETURN)
    # time.sleep(5)
    logging.debug("Поиск поля ввода даты С и ввод даты")
    input_from = browser.find_element(By.CSS_SELECTOR, 'span.from input.form-control')
    input_from.clear()
    input_from.send_keys(filter_date)  # с 01.12.2021
    input_from.send_keys(Keys.RETURN)
    logging.debug("Поиск поля ввода даты ПО и ввод даты")
    input_to = browser.find_element(By.CSS_SELECTOR, 'span.to input.form-control')
    input_to.clear()
    input_to.send_keys(filter_date)  # по 01.12.2021
    input_to.send_keys(Keys.RETURN)
    # time.sleep(5)


def init_webdriver(settings):
    logging.debug(f"headless={settings['headless']}")
    logging.debug(f"chromedriver_path={settings['chromedriver_path']}")
    if settings['headless']:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(settings['chromedriver_path'], options=chrome_options)
    else:
        browser = webdriver.Chrome(settings['chromedriver_path'])
    logging.debug(f"browser={browser}")
    return browser


def login_to_getcourse(browser, env):
    # Login в GetCourse
    logging.debug("Try login to GetCourse")
    browser.get("https://givin.school/cms/system/login?required=true")
    logging.debug("Find input login")
    input_login = browser.find_element(By.CSS_SELECTOR, "input.form-control.form-field-email")
    input_login.send_keys(env[0])
    logging.debug("Find input password")
    input_password = browser.find_element(By.CSS_SELECTOR, "input.form-control.form-field-password")
    input_password.send_keys(env[1])
    logging.debug("Find button ОК")
    button = browser.find_element(By.CSS_SELECTOR, ".float-row > .btn-success")
    button.click()
    time.sleep(5)


def filter3_columns(browser):
    # Поиск кнопки Колонки и чекнуть все Колонки
    logging.debug("Поиск кнопки Колонки")
    button_columns = browser.find_element(By.CSS_SELECTOR, "div.gc-grouped-selector")
    button_columns.click()
    logging.debug("Поиск последнего модального селектора")
    modal_windows = browser.find_elements(By.CSS_SELECTOR, "div.gc-grouped-selector-settings")
    last_modal_window = modal_windows[-1]
    logging.debug("Поиск основного меню и клик по всем пунктам")
    menus = last_modal_window.find_elements(By.CSS_SELECTOR, "div.li-label")
    for menu_item in menus:
        menu_item.click()
    logging.debug("Клик по всем пунктам")
    checkboxes = last_modal_window.find_elements(By.TAG_NAME, "input")
    for checkbox in checkboxes:
        checked = checkbox.get_attribute('checked')
        if checked:
            logging.debug("checked")
        else:
            logging.debug("not checked")
            checkbox.click()
    logging.debug("Поиск кнопки Apply")
    apply_buttons = browser.find_elements(By.CSS_SELECTOR, "button.btn.btn-save.btn-success")
    apply_button = apply_buttons[-1]
    apply_button.click()
    # time.sleep(5)


def filter1_add_conditions(browser):
    # Поиск кнопки Добавить условие и выбор в меню Авторизованный
    logging.debug("Поиск кнопки Добавить условие")
    button_show_more = browser.find_element(By.CSS_SELECTOR, "button.btn.btn-default.dropdown")
    button_show_more.click()
    logging.debug("Поиск поля ввода")
    search_input = browser.find_element(By.CSS_SELECTOR, "input.search-input")
    search_input.clear()
    search_input.send_keys("Ав")  # Авторизованный
    # search_input.send_keys(Keys.ENTER)  # В этом поле ENTER не срабатывает, нужно кликать на пункт меню
    logging.debug("Поиск пункта меню Авторизованный")
    menu_item = browser.find_element(By.CSS_SELECTOR, '[data-type="is_user"]')
    menu_item.click()
    # time.sleep(5)
