import logging
from selenium import webdriver


def parse_sessions():
    logging.info(f"Start parse sessions")
    try:
        logger.debug(f"headless={PASSWORDS.settings['headless']}")
        logger.debug(f"chromedriver_path={PASSWORDS.settings['chromedriver_path']}")
        if PASSWORDS.settings['headless']:
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--headless")
            browser = webdriver.Chrome(PASSWORDS.settings['chromedriver_path'], options=chromeOptions)
        else:
            browser = webdriver.Chrome(PASSWORDS.settings['chromedriver_path'])
        logger.debug(f"browser={browser}")
        # Вход в GetCourse иначе страница заказа будет недоступна
        logger.debug("Try login to GetCourse")
        browser.get(PASSWORDS.settings['getcourse_login_page'])
        input_login = browser.find_element_by_css_selector("input.form-control.form-field-email")
        input_login.send_keys(PASSWORDS.settings['getcourse_login'])
        input_password = browser.find_element_by_css_selector("input.form-control.form-field-password")
        input_password.send_keys(PASSWORDS.settings['getcourse_password'])
        button = browser.find_element_by_css_selector(".float-row > .btn-success")
        button.click()
        time.sleep(10)
        # Выделить из ссылки заказа ID и открыть страницу заказа (ссылка которая в письме не открывается)
        logger.debug("Выделить из ссылки заказа ID и открыть страницу заказа")
        link_id = link.rsplit("/", 1)
        link = "https://givinschoolru.getcourse.ru/sales/control/deal/update/id/" + link_id[1]
        logger.debug(f"link={link}")
        browser.get(link)
        time.sleep(10)
        # Поиск email на странице заказа
        logger.debug("Поиск email на странице заказа")
        email_element = browser.find_element_by_css_selector("div.user-email")
        logger.debug(f"email_element.text={email_element.text}")
        email = email_element.text
        if len(email) < 0:
            logger.warning(f"PARSING: Не нашел email на странице заказа - {link}")
        else:
            # print(f"email={email}")
            payment["Электронная почта"] = email
            logger.info(f"PARSING: email={email}")
        # Поиск telegram на странице заказа
        # telegram вариант 2 (только первый div может содержать telegram)
        logger.debug("Поиск telegram на странице заказа. Вариант 2")
        telegram_elements = browser.find_elements_by_xpath(
            "//*[contains(text(), 'Ник телеграмм')]/following-sibling::div")
        result = None
        if len(telegram_elements) == 0:
            logger.info("PARSING: На странице нет элемента 'Ник телеграмм'")
        else:
            logger.debug(f"telegram_elements[0].text={telegram_elements[0].text}")
            result = get_telegram_from_text(telegram_elements[0].text, logger)
        if not result:
            # telegram вариант 1 (здесь несколько равнозначных блоков из них выделяется телеграм, можно по идее брать
            # только второй блок)
            logger.debug("Поиск telegram на странице заказа. Вариант 1")
            telegram_elements = browser.find_elements_by_css_selector(".text-block>div[style]")
            if len(telegram_elements) > 0:
                text = ""
                for telegram_element in telegram_elements:
                    text += telegram_element.text
                result = get_telegram_from_text(text, logger)
        if result:
            print(f"telegram={result}")
            payment["telegram"] = result
            logger.info(f"PARSING: telegram={result}")
        else:
            logger.warning(f"PARSING: Не нашел telegram на странице заказа - {link}")
        # закрываем браузер после всех манипуляций
        logger.debug("закрываем браузер после всех манипуляций")
        browser.quit()
        logger.debug("payment_normalization(payment)")
        payment_normalization(payment)
    except:  # noqa: E722
        send_error_to_admin("ERROR: Ошибка парсинга страницы заказа GetCourse", logger, prog_name="payment_creator.py")
    finally:
        # закрываем браузер даже в случае ошибки
        browser.quit()
    logging.info(f"End parse sessions")
