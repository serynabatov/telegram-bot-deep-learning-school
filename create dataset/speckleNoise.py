import numpy as np
from PIL import Image
from createAdditionalFiles import AbstractNoise


class SpeckleNoise(AbstractNoise):

    def __init__(self, image):
        self.image = np.array(image)
        self.row, self.col, self.ch = self.image.shape

    def __create_noise__(self):
        gauss = np.random.randn(self.row, self.col, self.ch)
        gauss = gauss.reshape(self.row, self.col, self.ch)
        noise = self.image + self.image * gauss/2
        return Image.fromarray(noise.astype(np.uint8))


if __name__ == "__main__":
    some_im = Image.open('1_10_58.jpg')
    g = SpeckleNoise(some_im)
    gau_im = g.__create_noise__()
    gau_im.save('../ex4.jpg')
