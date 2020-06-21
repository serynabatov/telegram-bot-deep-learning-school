from abc import ABC, abstractmethod
import os


class AbstractNoise(ABC):

    @abstractmethod
    def __create_noise__(self):
        pass

    def create_image(self, name, directory_noise):
        if not os.path.exists(".\\{}".format(directory_noise)):
            os.mkdir(".\\{}".format(directory_noise))
        im = self.__create_noise__()
        im.save(".\\{}\\{}".format(directory_noise, name))
