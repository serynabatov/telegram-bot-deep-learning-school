from searchingWithGoogle import GoogleSearchImages
from searchingWithYandex import YandexSearchImages
from langdetect import detect
import pyautogui


class DataSetLoad:

    def __init__(self, site, query, number):
        assert number < 1000, "Меньше 1000 ставьте."
        self.number = number
        if site.lower() == 'google':
            self.object = GoogleSearchImages()
        else:
            assert detect(query) != 'rus', "Пожалуйста, для яндекса пишите по русски."
            self.object = YandexSearchImages()
        self.query = query

    def load(self):
        self.object.search(self.query)
        self.object.download(self.number)


if __name__ == "__main__":
    # Загрузим фотографии
    image = DataSetLoad('yandex', 'публикация в статье', 10)

    image.load()
