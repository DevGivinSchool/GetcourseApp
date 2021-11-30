import logging
import urls
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from error_handling import error_handler as error_handler


def parse_sessions(settings, env):
    logging.info(f"Start parse sessions")
    try:
        logging.debug(f"headless={settings['headless']}")
        logging.debug(f"chromedriver_path={settings['chromedriver_path']}")
        if settings['headless']:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            browser = webdriver.Chrome(settings['chromedriver_path'], options=chrome_options)
        else:
            browser = webdriver.Chrome(settings['chromedriver_path'])
        logging.debug(f"browser={browser}")

        # browser.implicitly_wait(10)  # seconds

        # Вход в GetCourse иначе страница заказа будет недоступна
        logging.debug("Try login to GetCourse")
        browser.get("https://givin.school/cms/system/login?required=true")  # TODO
        input_login = browser.find_element(By.CSS_SELECTOR, "input.form-control.form-field-email")
        input_login.send_keys(env[0])
        input_password = browser.find_element(By.CSS_SELECTOR, "input.form-control.form-field-password")
        input_password.send_keys(env[1])
        button = browser.find_element(By.CSS_SELECTOR, ".float-row > .btn-success")
        button.click()
        time.sleep(5)

        # Выделить из ссылки заказа ID и открыть страницу заказа (ссылка которая в письме не открывается)
        logging.debug("Открыть страницу sessions")
        logging.debug(f"link={urls.base_url}")
        browser.get(urls.base_url)
        time.sleep(5)

        # Поиск кнопки Добавить условие
        logging.debug("Поиск кнопки Добавить условие")
        button_show_more = browser.find_element(By.CSS_SELECTOR, "button.btn.btn-default.dropdown")
        button_show_more.click()
        search_input = browser.find_element(By.CSS_SELECTOR, "input.search-input")
        search_input.clear()
        search_input.send_keys("Авторизованный")
        menu_item = browser.find_element(By.CSS_SELECTOR, '[data-type="is_user"]')
        menu_item.click()
        time.sleep(5)

        # Поиск кнопки Показать еще
        # logging.debug("Поиск кнопки Показать еще")
        # button_show_more = browser.find_element(By.CSS_SELECTOR, "a.btn.btn-default")
        # logging.debug(f"button_show_more.text={button_show_more.text}")

        # закрываем браузер после всех манипуляций
        logging.debug("Закрываем браузер после всех манипуляций")
        browser.quit()
    except Exception as e:  # noqa: E722
        error_handler("Ошибка парсинга страницы", do_exit=True)
    finally:
        # закрываем браузер даже в случае ошибки
        browser.quit()
    logging.info(f"End parse sessions")
