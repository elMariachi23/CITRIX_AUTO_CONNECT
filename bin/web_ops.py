from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time


def open_citrix(link):
    """
    Запуск ссылки для CITRIX
    :param link: адрес для подключения
    :return browser: Объект подключения браузера к ссылке
    """
    browser = webdriver.Firefox()
    browser.get(link)
    assert "Citrix Gateway" in browser.title
    return browser


def login_citrix(browser, login, password, key_word):
    """
    Авторизация в CITRIX
    :param browser: Объект подключения к браузеру
    :param login: Логин (УЗ)
    :param password: Пароль (Доменный)
    :param key_word: Кодовое слово (второй пароль)
    :return: Boolean успешности ввода авторизации
    """
    # Ожидание загрузки всех элементов страницы
    try:
        browser.maximize_window()
        browser.implicitly_wait(10)
        elem = browser.find_element_by_css_selector(r'#Enter\ user\ name')
        elem.send_keys(login)
        elem = browser.find_element_by_css_selector(r'#passwd')
        elem.send_keys(password)
        elem = browser.find_element_by_css_selector(r'#passwd1')
        elem.send_keys(key_word)
        elem.send_keys(Keys.ENTER)
        # submit = browser.find_element_by_css_selector(r'#Log_On')
        # submit.click()
        return True
    except TimeoutException:
        logging.error('Таймаут ожидания загрузки элемента страницы')
        return False


def inter_pincode(browser, pin):
    """
    Передача пин-кода в Citrix для прохождения двухфакторной аутентификации
    :param browser: Объект подключения к браузеру
    :param pin: Пин-код полученный от Citrix по СМС
    :return: Boolean
    """
    try:
        browser.implicitly_wait(10)
        code_in = browser.find_element_by_css_selector(r'#response')
        code_in.send_keys(pin)
        submit = browser.find_element_by_css_selector(r'#SubmitButton')
        # submit.click()
        code_in.send_keys(Keys.ENTER)
        # browser.implicitly_wait(10)
        # reciever = browser.find_element_by_css_selector(r'#protocolhandler-welcome-installButton')
        # ActionChains(browser).move_to_element(reciever).click(reciever).perform()
        return True
    except TimeoutException:
        logging.error('Таймаут ожидания загрузки элемента страницы')
        return False


def load_vdi_file(browser):
    """
    Загрузка файла, для доступа к VDI
    :param browser: Объект подключения к браузеру
    :return:
    """
    try:
        browser.implicitly_wait(10)
        # link = browser.find_element_by_css_selector(r'#a.storeapp-details-link')
        link = browser.find_element_by_id('storeapp-details-link')
        link.click()
    except TimeoutException:
        logging.error('Таймаут ожидания загрузки элемента страницы')
        return False


def test():
    """
    Функция тестирования модуля
    :return:
    """
    #     x:708 y:45
    # time.sleep(3)
    x, y = pyautogui.position()
    print('x:{} y:{}'.format(x, y))
    # pyautogui.moveTo(708, 87)
    # pyautogui.click(button='left')
    # time.sleep(3)


if __name__ == '__main__':
    # test()
    pass
