# create table settings
sql_ct_last_date = "CREATE TABLE last_date (value TEXT)"

# create table sessions
'''
ID визита
Начало визита
IP
Тип трафика
Канал
Глубина просмотра
Номер визита
ID посетителя
Устройство
Страница входа
Адрес входа
Referrer входа
Пользователь
Заказ
Группа каналов
Группа расходов
Группа расходов
Кампания
UTM-medium
UTM-source
Ключевое слово
UTM-Content
Реферер - значимый домен
Реферер - домен
Реферер
Страница старта
Глубина просмотра
Есть заказ
Есть заказ
'''
sql_ct_sessions = """CREATE TABLE sessions (name, value)"""
