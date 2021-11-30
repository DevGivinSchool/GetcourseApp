import logging
from selenium import webdriver


def parse_sessions(settings, env):
    logging.info(f"Start parse sessions")
    try:
        logging.debug(f"headless={settings['headless']}")
        logging.debug(f"chromedriver_path={settings['chromedriver_path']}")
        if settings['headless']:
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--headless")
            browser = webdriver.Chrome(settings['chromedriver_path'], options=chromeOptions)
        else:
            browser = webdriver.Chrome(settings['chromedriver_path'])
        logging.debug(f"browser={browser}")

        # Вход в GetCourse иначе страница заказа будет недоступна
        logging.debug("Try login to GetCourse")
        browser.get(settings['getcourse_login_page'])  # TODO
        input_login = browser.find_element_by_css_selector("input.form-control.form-field-email")
        input_login.send_keys(env[0])
        input_password = browser.find_element_by_css_selector("input.form-control.form-field-password")
        input_password.send_keys(PASSWORDS.settings[env[1]])
        button = browser.find_element_by_css_selector(".float-row > .btn-success")
        button.click()
        time.sleep(10)

        # Выделить из ссылки заказа ID и открыть страницу заказа (ссылка которая в письме не открывается)
        logging.debug("Выделить из ссылки заказа ID и открыть страницу заказа")
        link_id = link.rsplit("/", 1)
        link = "https://givinschoolru.getcourse.ru/sales/control/deal/update/id/" + link_id[1]
        logger.debug(f"link={link}")
        browser.get(link)
        time.sleep(10)

        # Поиск email на странице заказа
        logging.debug("Поиск email на странице заказа")
        email_element = browser.find_element_by_css_selector("div.user-email")
        logging.debug(f"email_element.text={email_element.text}")
        email = email_element.text
        if len(email) < 0:
            logging.warning(f"PARSING: Не нашел email на странице заказа - {link}")
        else:
            # print(f"email={email}")
            payment["Электронная почта"] = email
            logger.info(f"PARSING: email={email}")

        # закрываем браузер после всех манипуляций
        logging.debug("закрываем браузер после всех манипуляций")
        browser.quit()
    except:  # noqa: E722
        send_error_to_admin("ERROR: Ошибка парсинга страницы заказа GetCourse", logger, prog_name="payment_creator.py")
    finally:
        # закрываем браузер даже в случае ошибки
        browser.quit()
    logging.info(f"End parse sessions")
