import pyautogui


def check_monitor_size():
    """
    Функция определения какой монитор используется
    и передача соответствующих координат кнопок
    :return: Координаты необходимых кнопок, взависимости от монитора
    """
    mon_size = pyautogui.size()
    print(mon_size)
    if mon_size.width == 1920 and mon_size.height == 1080:
        citrix_button = 105, 372
        enter_button = 1112, 646
    elif mon_size.width == 2560 and mon_size.height == 1440:
        citrix_button = 105, 372
        enter_button = 1431, 829
    else:
        citrix_button = 103, 377
        enter_button = 873, 569
    return citrix_button, enter_button


def drill_to_reciever():
    """
    Имитация действий мыши
    :return:
    """
    cit_btn, enter_btn = check_monitor_size()
    pyautogui.sleep(5)
    pyautogui.click(cit_btn)
    pyautogui.sleep(5)
    pyautogui.click(enter_btn)
    pyautogui.sleep(5)
    pyautogui.press('Enter')


if __name__ == '__main__':
    x, y = pyautogui.position()
    print(x, y)
    check_monitor_size()

