# SessionParser

## Полезные сведения
Данные session начинаются с 2019-05-18 17:29:52 (18.05.2019)  
Дата для тестирования - 19.11.2019  

## Ошибки
### Ошибка: Какой-то элемент CSS не найден на странице
```python
email_element = browser.find_element(By.CSS_SELECTOR, "div.user-email")
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"div.user-email"
```
Можно попробовать увеличить параметр `TIMEOUT = 1  # timeout in sec` в файле `parser.py`.  

## Документация
[Selenium with Python](https://selenium-python.readthedocs.io/)
[BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/index.html)

## Update requirements
```
pip freeze | Out-File -Encoding UTF8 requirements.txt
```
## Список столбцов
visit_id	ID визита	'749780063'
start_of_visit	Начало визита	'2019-11-19 22:52:23'
ip	IP	'RU, Калининградская область, Калининград 83.219.136.214'
traffic_type	Тип трафика	'Внутренние переходы'
channel	Канал	'internal:givinschoolru.getcourse.ru'
depth_of_view	Глубина просмотра	'4'
visit_number	Номер визита	'2'
visitor_id	ID посетителя	'580563057'
device	Устройство	'Desktop'
login_page	Страница входа	'https://givinschoolru.getcourse.ru/pl/teach/control/lesson/view'
entrance_address	Адрес входа	https://givinschoolru.getcourse.ru/pl/teach/control/lesson/view?id=96894255'
login_referrer	Referrer входа	'https://givinschoolru.getcourse.ru/pl/teach/control/lesson/view?id=96795704&editMode=0'
user	Пользователь	'АНТОН АНУЧИН'
order	Заказ	'-- пусто --'
channel_group	Группа каналов	'internal:givinschoolru.getcourse.ru'
expense_group_1	Группа расходов	'internal:givinschoolru.getcourse.ru'
expense_group_2	Группа расходов	'internal:givinschoolru.getcourse.ru'
campaign	Кампания	'-- без кампании --'
utm_medium	UTM-medium	'-- пусто --'
utm_source	UTM-source	'-- пусто --'
keyword	Ключевое слово	'-- пусто --'
utm_content	UTM-Content	'-- пусто --'
referrer_significant_domain	Реферер - значимый домен	'getcourse'
referrer_domain	Реферер - домен	'givinschoolru.getcourse.ru'
referrer	Реферер	'https://givinschoolru.getcourse.ru/pl/teach/control/lesson/view?id=96795704&editMode=0'
start_page	Страница старта	'https://givinschoolru.getcourse.ru/pl/teach/control/lesson/view?id=96894255'
depth_of_view	Глубина просмотра	'-- пусто --'
there_is_an_order_1	Есть заказ	'-- пусто --'
there_is_an_order_2	Есть заказ	'-- пусто --'
country	Страна	RU'
region	Регион	Краснодарский край'
city	Город	Туапсе'
ip2	IP адрес	188.43.12.65'
user_id	ID Пользователя	59947508'
user_url	Ссылка на профиль Пользователя	/user/control/user/update/id/59947508'
user_email	email профиль пользователя	email@mail.ru
user_telegram	telegram профиль пользователя	@telegram
user_country	country профиль пользователя	Россия
user_city	city профиль пользователя	Сочи
user_phone  phone   Телефон пользователя
