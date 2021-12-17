import logging
import sqlite3
import sql
from error_handling import error_handler as error_handler


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        return conn
    except Error as e:
        error_handler(str(e), do_exit=True)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        error_handler(str(e), do_exit=True)


def select_all(conn, sql_text):
    c = conn.cursor()
    c.execute(sql_text)
    result = c.fetchall()
    return result


def select_one(conn, sql_text):
    c = conn.cursor()
    c.execute(sql_text)
    result = c.fetchone()
    return result


def init_database():
    conn: Connection = None
    try:
        conn = create_connection('sp.db')
        cursor = conn.cursor()
        logging.info("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "select sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()  # record is list of tuples [('3.35.5',)]
        logging.info(f"Версия базы данных SQLite: {record[0][0]}")

        create_table(conn, sql.sql_ct_last_date)
        logging.info("...Создана таблица last_date")
        create_table(conn, sql.sql_ct_sessions)
        logging.info("...Создана таблица sessions")

        cursor.close()

    except sqlite3.Error as error:
        logging.info(f"Ошибка инициализации БД {error}")
    finally:
        if conn:
            conn.close()
            logging.debug("Соединение с БД закрыто")


def fill_sessions_table(conn, raw_data, last_date):
    data = []
    for line in raw_data:
        data.append(tuple(line))
    conn.isolation_level = None
    c = conn.cursor()
    c.execute("begin")
    try:
        # Fill the table
        c.executemany("insert into sessions (visit_id,start_of_visit,ip,traffic_type,channel,depth_of_view1,"
                      "visit_number,visitor_id,device,login_page,entrance_address,login_referrer,user,order1,"
                      "channel_group,expense_group_1,expense_group_2,campaign,utm_medium,utm_source,keyword,"
                      "utm_content,referrer_significant_domain,referrer_domain,referrer,start_page,depth_of_view2,"
                      "there_is_an_order_1,there_is_an_order_2,country,region,city,ip2,user_id,user_url,user_email,"
                      "user_telegram,user_country,user_city) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                      "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        c.execute("insert into last_date (value) values (?)", (last_date,))
        c.execute("commit")
    except conn.Error as e:
        c.execute("rollback")
        error_handler(str(e), do_exit=True)
    # Print the table contents
    # for row in c.execute("select * from sessions"):
    #     print(row)
