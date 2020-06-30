from torchvision import transforms, utils
from torch.utils.data import Dataset, DataLoader
import numpy as np
from PIL import Image
from model_GAN import ResnetGenerator
import torch
import asyncio


async def imshow(inp):
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.5, 0.5, 0.5])
    std = np.array([0.5, 0.5, 0.5])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    return inp

async def test(te_dataset, model, loop=None):
    test_loader = DataLoader(te_dataset, batch_size=1)

    data = next(iter(test_loader))

    fake_B = model(data.to('cpu'))

    image_fake = await loop.create_task(imshow(fake_B[0].data.cpu()))


    return image_fake


class ModelDataset(Dataset):


    def __init__(self, image, augmentation=None):
        super().__init__()

        self.image = image
        self.augmentation = augmentation


    def __getitem__(self, index):
        A = np.array(np.array(self.image) / 255, dtype='float32')
        A = self.augmentation(Image.fromarray((A*255).astype('uint8')))
        return A

    def __len__(self):
        return 1

    def create_batch(self, im):
        im = im[:3, :, :].unsqueeze(0)
        return im

if __name__=="__main__":
    dataset = ModelDataset('./ss.jpg')
    model = ResnetGenerator()
    model.load_state_dict(torch.load('./model_gen_BtoA1.pth', map_location=torch.device('cpu')))
    print(test(dataset, model))
