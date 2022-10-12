import configparser
import datetime
import os
import logging
import logging.config
import stat
import web_ops
import message_ops
import mouse_work


def main():
    """
    Основная логика
    :return:
    """

    citrix_adr = config.get('CITRIX', 'address')
    logging.info('Этап: Запуск Firefox и Переход по ссылке CITRIX "{}"'.format(citrix_adr))
    ctx = web_ops.open_citrix(citrix_adr)
    stage_result()

    logging.info('Этап: Авторизация')
    citrix_login = config.get('CITRIX_AUTH', 'login')
    citrix_pass = config.get('CITRIX_AUTH', 'password')
    citrix_keyword = config.get('CITRIX_AUTH', 'key_word')
    if web_ops.login_citrix(ctx, citrix_login, citrix_pass, citrix_keyword):
        stage_result()
    else:
        stage_result(False)
        exit()
    logging.info('Этап: Поиск пин-кода для CITRIX')
    now = datetime.datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    msg_db = config.get('MSG_DB', 'file')
    ctx_number = config.get('CITRIX', 'mobile_number')
    code = message_ops.citrix_pin(msg_db, ctx_number, current_datetime)
    logging.debug('Получен пин-код от Citrix: {}'.format(code))
    logging.info('Этап: Ввод пин-кода')
    if web_ops.inter_pincode(ctx, code):
        stage_result()
    else:
        stage_result(False)
        exit()
    logging.info('Этап: Имитация мыши, подключение к VDI')
    mouse_work.drill_to_reciever()
    stage_result()


def set_logging():
    """
    Настройка логирования
    :return:
    """
    log_dir = 'logs'
    log = 'connect.log'
    logfile_name = log_dir + '/' + log

    # Проверка на существование папки для логов
    if log_dir not in os.listdir(script_home):
        os.makedirs(log_dir, 0o777)

    if log not in os.listdir(log_dir):
        open(logfile_name, 'w').close()
        os.chmod(logfile_name, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)


def stage_result(flag=True):
    """
    Логирование результата этапа
    :param flag: Флаг выполнения
    :return: None
    """
    if flag:
        logging.info('Готово!')
    else:
        logging.error('Ошибка')


if __name__ == '__main__':
    # Расположение Кода
    script_home = os.path.dirname(os.path.abspath(__file__))
    script_home = script_home + '/../'
    os.chdir(script_home)

    set_logging()
    logging.config.fileConfig('conf/logging.conf')

    logging.info('Выполнен запуск')

    # Загрузка конфигурации
    config = configparser.ConfigParser()
    config.read('conf/configuration.ini')

    # Запуск основной логики
    try:
        main()
    finally:
        pass
