import sqlite3
import logging
import time
from datetime import datetime
import re


def citrix_pin(db, citrix_number, date):
    """
    Операции по получению пин-кода от CITRIX
    :param db: Путь до базы сообщений
    :param citrix_number: Номер телефона с которого CITRIX отправляет пин-код
    :param date: Дата проверки
    :return code: Пин-код
    """
    conn = connect_to_db(db)
    cur = conn.cursor()
    logging.debug('Получены параметры...')
    logging.debug('Номер телефона CITRIX: {}'.format(citrix_number))
    logging.debug('Текущая дата: {}'.format(date))
    cur.execute("select ROWID from handle where id = '" + citrix_number + "'")
    rowid = cur.fetchone()
    rowid = str(rowid[0])
    message_date = 'datetime(date / 1000000000 + strftime("%s", "2001-01-01 00:00:00"), "unixepoch", "localtime")'
    while True:
        cur.execute("select text, " + message_date + " from message where handle_id = '" + rowid + "' "
                    "order by date desc")
        result = cur.fetchone()
        text = result[0]
        msg_date = result[1]
        if date > msg_date:
            logging.debug('Ожидается сообщение от CITRIX')
            time.sleep(3)
            continue
        else:
            logging.debug(text)
            return parse_msg(text)


def connect_to_db(db_name):
    """
    Подключение к базе
    :param db_name: Имя базы данных/путь до файла с базой данных
    :return connection: Объект подключения к БД
    """
    connection = sqlite3.connect(db_name)
    logging.debug('Выполнено подключение к базе: {}'.format(db_name))
    return connection


def parse_msg(msg):
    """
    Функция поиска Пин-кода в тексте сообщения
    :param msg: Полный текст сообщения
    :return pin: Пин-код
    """
    pin = re.findall(r'\d{2,}', msg)[0]
    return pin


def test():
    try:
        conn = connect_to_db('/Users/Sergey/Library/Messages/chat.db')
        cur = conn.cursor()
        cur.execute("select ROWID from handle where id = '+79160001642'")
        # names = [description[0] for description in cur.description]
        rowid = cur.fetchone()
        date = 'datetime(date / 1000000000 + strftime("%s", "2001-01-01 00:00:00"), "unixepoch", "localtime")'
        # print(names)
        cur.execute("select text, " + date + " from message where handle_id = '" + str(rowid[0]) + "' "
                    "order by date desc")
        result = cur.fetchone()
        # date = result[1] / 1000000000 + strftime("%s", "2001-01-01")
        print(result)
        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        if current_datetime < result[1]:
            print('Cur is newer')

    except Exception as err:
        print(err)
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass


if __name__ == '__main__':
    # test()
    parse_msg('On demand token: 955287 expires after use or 3 minutes')
