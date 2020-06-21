from gaussNoise import GaussNoise
from poissonNoise import PoissonNoise
from replaceRandomPixels import SaltAndPepper
from speckleNoise import SpeckleNoise
import shutil
import os
from PIL import Image


def rename_images(directory, to_directory):
    i = 0
    for fileName in sorted(os.listdir(directory)):
        if not os.path.exists("{}".format(to_directory)):
            os.mkdir("{}".format(to_directory))
        if fileName.endswith('.jpg'):
            # if i == 270:
            #     print(fileName)
            if not os.path.exists("{}{}".format(to_directory, fileName)):
                shutil.copy("{}{}".format(directory, fileName), "{}\\{}.jpg".format(to_directory, i))
                i += 1


if __name__ == "__main__":
    rename_images("..\\..\\Dataset\\1\\", "..\\..\\Dataset\\original\\")

    os.chdir('..\\..\\Dataset\\original\\')

    for image in sorted(os.listdir('.\\')):

        if image.endswith('.jpg'):
            im = Image.open(image)
            g = GaussNoise(im)
            p = PoissonNoise(im)
            s = SpeckleNoise(im)
            s_p = SaltAndPepper(im)

            g.create_image(image, "..\\gauss_test")
            p.create_image(image, "..\\poisson_test")
            s.create_image(image, "..\\speckle_test")
            s_p.create_image(image, "..\\saltandpepper_test")
