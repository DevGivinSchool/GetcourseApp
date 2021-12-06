import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from error_handling import error_handler as error_handler


def parse_sessions_one_day(settings, env, filter_date: str):
    logging.info(f"Start parse sessions")
    try:
        browser = init_webdriver(settings)

        login_to_getcourse(browser, env)

        # Открыть страницу sessions
        logging.debug("Открыть страницу Трафик - Сессии")
        logging.debug("link=https://givin.school/pl/metrika/traffic/visit-list")
        browser.get("https://givin.school/pl/metrika/traffic/visit-list")
        time.sleep(5)

        filter1_add_conditions(browser)  # Кнопка "Добавить условие" и выбор в меню пункта "Авторизованный"
        filter3_columns(browser)         # Кнопка "Колонки" и чекнуть все колонки
        filter2_select_dates(browser, filter_date)    # Кнопка "Выбрать даты" и заполнение полей дат

        # Здесь кликаю по h1 просто чтобы выйти из поля даты
        logging.debug("Поиск h1")
        div_h1 = browser.find_element(By.TAG_NAME, "h1")
        div_h1.click()
        # time.sleep(5)

        # Поиск кнопки Показать еще. Её нужно кликнуть столько раз чтобы список раскрылся полностью.
        logging.debug("Поиск кнопки Выбрать даты")
        count_button_show_more1 = 0
        list_button_show_more = browser.find_elements(By.CSS_SELECTOR, "a.btn.btn-default")
        count_button_show_more1 = len(list_button_show_more)
        logging.debug(f"count_button_show_more = {count_button_show_more}")
        if count_button_show_more1>0:
            
        # button_show_more.click()


        # Пауза чтобы рассмотреть результат
        time.sleep(30)

        # закрываем браузер после всех манипуляций
        logging.debug("Закрываем браузер после всех манипуляций")
        browser.quit()
    except Exception as e:  # noqa: E722
        error_handler("Ошибка парсинга страницы", do_exit=True)
    finally:
        # закрываем браузер даже в случае ошибки
        browser.quit()
    logging.info(f"End parse sessions")


def filter2_select_dates(browser, filter_date):
    # Поиск кнопки Выбрать даты и заполнение полей дат
    logging.debug("Поиск кнопки Выбрать даты")
    button_select_dates = browser.find_element(By.CSS_SELECTOR, "span#select2-chosen-4.select2-chosen")
    button_select_dates.click()
    logging.debug("Поиск поля ввода и выбор пункта Выбрать даты")
    search_input = browser.find_element(By.CSS_SELECTOR, "input#s2id_autogen4_search.select2-input")
    search_input.clear()
    search_input.send_keys("Выбрать даты")  # Выбрать даты
    search_input.send_keys(Keys.ENTER)
    # time.sleep(5)
    logging.debug("Поиск поля ввода даты С и ввод даты")
    input_from = browser.find_element(By.CSS_SELECTOR, 'span.from input.form-control')
    input_from.clear()
    input_from.send_keys(filter_date)  # с 01.12.2021
    input_from.send_keys(Keys.ENTER)
    logging.debug("Поиск поля ввода даты ПО и ввод даты")
    input_to = browser.find_element(By.CSS_SELECTOR, 'span.to input.form-control')
    input_to.clear()
    input_to.send_keys(filter_date)  # по 01.12.2021
    input_to.send_keys(Keys.ENTER)
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
