from abstract_strat import Abstract_Strategy
from io import BytesIO
from dataset import ModelDataset, test
from model_GAN import ResnetGenerator
import torch
import torch.nn as nn
import asyncio
from torchvision import transforms, models
from PIL import Image
from normaliz import Normalization
from style_loss import StyleLoss
from gram import GramMatrix
from content_loss import ContentLoss
import numpy as np


class Gogh(Abstract_Strategy):

    def __init__(self):
        self.imgByteArr = BytesIO()
        self.trans = transforms.ToPILImage()
        self.augmentation = transforms.Compose([
                                      transforms.Resize((256, 256)),
                                      transforms.ToTensor(),
                                      transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    async def send_to_net(self, image, loop=None):
        dataset = ModelDataset(image, self.augmentation)
        model = ResnetGenerator()
        model.load_state_dict(torch.load('/opt/app/model_gen_BtoA2.pth', 
                                          map_location=torch.device('cpu')))
        image1 = await loop.create_task(test(dataset, model, loop))
        image1 = Image.fromarray((image1 * 255).astype('uint8'))
        image1.save(self.imgByteArr, 'JPEG')
        im = self.imgByteArr.getvalue()
        return im


class Transfer(Abstract_Strategy):

    def __init__(self):
       self.imgByteArr = BytesIO()
       self.augmentation = transforms.Compose([
                                     transforms.Resize((256, 256)),
                                     transforms.ToTensor()
       ])

    def ready_to_show(self, im, loop=None):
       im = im.numpy().transpose((1, 2, 0))
       im = np.clip(im, 0, 1)
       return im

    async def send_to_net(self, image_style, image_content, loop=None):
       print('k')
       model = models.vgg19(pretrained=False).features
       model = nn.DataParallel(model)

       model.module.load_state_dict(torch.load('/opt/app/content.pth', map_location=torch.device('cpu')), strict=True)

       model = model.module.eval()

       style_in = ModelDataset(image_style, self.augmentation)
       style = style_in.create_batch(style_in[0])
       content_in = ModelDataset(image_content, self.augmentation)
       content = content_in.create_batch(content_in[0])
       input = content.clone()

       #input = torch.randn(content.data.size())
       optim = torch.optim.LBFGS([input.requires_grad_()])

       target_image = self.train(model, content, style, input, optim)
       target_im = self.ready_to_show(target_image[0].detach().cpu())

       image1 = Image.fromarray((target_im * 255).astype('uint8'))
       image1.save(self.imgByteArr, 'JPEG')
       im = self.imgByteArr.getvalue()

       return im

    def get_style_model_and_losses(self, cnn, style_img, content_img):
        content_layers= ['conv_4']
        style_layers = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5'] 
        normalization_mean = torch.tensor([0.485, 0.456, 0.406])
        normalization_std = torch.tensor([0.229, 0.224, 0.225])


        normalization = Normalization(normalization_mean, normalization_std)

        content_losses = []
        style_losses = []

        model = nn.Sequential(normalization)

        i = 0
        for layer in cnn.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = 'conv_{}'.format(i)
            elif isinstance(layer, nn.ReLU):
                name = 'relu_{}'.format(i)
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = 'pool_{}'.format(i)
            elif isinstance(layer, nn.BatchNorm2d):
                 name = 'bn_{}'.format(i)
            else:
                 raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))

            model.add_module(name, layer)

            if name in content_layers:

               target = model(content_img).detach()
               content_loss = ContentLoss(target)
               model.add_module("content_loss_{}".format(i), content_loss)
               content_losses.append(content_loss)

            if name in style_layers:
               target_feature = model(style_img).detach()
               style_loss = StyleLoss(target_feature)
               model.add_module("style_loss_{}".format(i), style_loss)
               style_losses.append(style_loss)

        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
                break

        model = model[:(i + 1)]

        return model, style_losses, content_losses


    def train(self, cnn, content_img, style_img, input_img, optimizer,  num_steps=100,
                       style_weight=1000, content_weight=0.01):


        model, style_losses, content_losses = self.get_style_model_and_losses(cnn,
                                                                             style_img, content_img)

        run = [0]
        while run[0] <= num_steps:

            def closure():

                input_img.data.clamp_(0, 1)

                optimizer.zero_grad()
                model(input_img)
                style_score = 0
                content_score = 0

                for sl in style_losses:
                    style_score += sl.loss
                for cl in content_losses:
                    content_score += cl.loss

                style_score *= style_weight
                content_score *= content_weight

                loss = style_score + content_score
                loss.backward()

                run[0] += 1


                return style_score + content_score

            optimizer.step(closure)


        input_img.data.clamp_(0, 1)

        return input_img

