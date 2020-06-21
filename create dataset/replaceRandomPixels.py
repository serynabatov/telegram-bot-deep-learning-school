import numpy as np
from PIL import Image
from createAdditionalFiles import AbstractNoise


class SaltAndPepper(AbstractNoise):

    def __init__(self, image):
        self.image = np.array(image)
        self.probability = 0.9
        self.row, self.col, self.ch = self.image.shape
        self.amount = 0.1
        self.output = np.copy(image)

    def __create_noise__(self):
        num_salt = np.ceil(self.amount * self.image.size * self.probability)
        coords1 = [np.random.randint(0, i - 1, int(num_salt)) for i in self.image.shape]
        self.output[tuple(coords1)] = 1

        num_pepper = np.ceil(self.amount * self.image.size * (1. - self.probability))
        coords2 = [np.random.randint(0, i - 1, int(num_pepper)) for i in self.image.shape]

        self.output[tuple(coords2)] = 0

        return Image.fromarray(self.output.astype(np.uint8))


if __name__ == "__main__":
    some_im = Image.open('1_10_58.jpg')
    g = SaltAndPepper(some_im)
    gau_im = g.__create_noise__()
    gau_im.save('../ex2.jpg')
