import numpy as np
from PIL import Image
from createAdditionalFiles import AbstractNoise


class PoissonNoise(AbstractNoise):

    def __init__(self, image):
        self.image = np.array(image)
        self.values = 2 ** np.ceil(np.log2(len(np.unique(image))))

    def __create_noise__(self):
        noise = np.random.poisson(self.image * self.values) / float(self.values)

        return Image.fromarray(noise.astype(np.uint8))


if __name__ == "__main__":
    some_im = Image.open('1_10_58.jpg')
    g = PoissonNoise(some_im)
    gau_im = g.__create_noise__()
    gau_im.save('../ex3.jpg')
