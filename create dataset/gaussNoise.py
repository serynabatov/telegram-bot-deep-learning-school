import numpy as np
from PIL import Image
from createAdditionalFiles import AbstractNoise


class GaussNoise(AbstractNoise):

    def __init__(self, image):
        self.image = image
        self.row, self.col = image.size
        self.ch = len(image.getbands())
        self.mean = 1.5
        self.var = 0.1
        self.sigma = self.var ** 0.5

    def __create_noise__(self):
        noise = np.random.normal(self.mean, self.sigma, (self.col, self.row, self.ch))
        noise = noise.reshape(self.col, self.row, self.ch)
        return Image.fromarray((noise + self.image).astype(np.uint8))


if __name__ == "__main__":
    some_im = Image.open('1_10_58.jpg')
    g = GaussNoise(some_im)
    gau_im = g.__create_noise__()
    gau_im.save('../ex.jpg')
