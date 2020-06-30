from PIL import Image


class Context:

    def __init__(self, strategy):

        self.strategy = strategy

    async def send(self, image, loop=None):

        if isinstance(image, list):
           print('lk')
           image_style = Image.open(image[0])
           image_context = Image.open(image[1])
           im = await loop.create_task(self.strategy.send_to_net(image_style, 
                                          image_context, loop))
        else:
           print('sssss')
           image = Image.open(image)
           im = await loop.create_task(self.strategy.send_to_net(image, loop))
        return im
