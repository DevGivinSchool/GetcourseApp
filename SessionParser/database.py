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
        logging.info("...Создана таблица settings")

        cursor.close()

    except sqlite3.Error as error:
        logging.info(f"Ошибка инициализации БД {error}")
    finally:
        if conn:
            conn.close()
            logging.debug("Соединение с БД закрыто")
