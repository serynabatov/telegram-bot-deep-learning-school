from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.touch_actions import TouchActions
import pyautogui
import time


# Данный класс используется для работы с веб браузером Chrome
class GoogleSearchImages:

    def __init__(self):
        # Конфигурируем дополнительные опции, которые запрещают использование w3c
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('w3c', False)
        # Создаем драйвер браузера
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        # Поскольку класс подразумевает поиск по гугл картинкам, хардкодим
        self.url = "https://images.google.com"

    def search(self, searching):
        # Передаем url драйверу для поиска определенного запроса
        self.driver.get(url=self.url)
        # Перемещаем курсор на строку "поиск"
        search_button = self.driver.find_element_by_class_name('gLFyf')
        search_button.click()
        # Передаем текстовый запрос поисковой строке
        search_button.send_keys(searching)
        search_button.submit()
        # Получаем текущий url
        self.url = self.driver.current_url

    def download(self, number):
        # Проверяем кол-во картинок
        assert number < 1000, "Так делать не стоит!"
        # Создаем объект для работы с окружением картинок
        touch_act = TouchActions(self.driver)

        # Берем первую картинку и нажимаем на нее
        elem = self.driver.find_element_by_class_name("rg_i")
        touch_act.tap(elem)
        touch_act.perform()

        # Выполняем процедуру сохранения
        for _ in range(number):
            pyautogui.press('apps')
            pyautogui.press('esc')
            time.sleep(1)
            pyautogui.press('apps')
            for _ in range(7):
                pyautogui.press('down')

            pyautogui.press('enter')
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(5)
            pyautogui.press('right')

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    search = GoogleSearchImages()
    search.search('document text')
    search.download(2000)
    try:
        del search
    except ImportError:
        pass
