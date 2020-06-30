import torch.nn as nn


class ResnetGenerator(nn.Module):

    def __init__(self):
        super().__init__()

        self.layer1 = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(3, 64, kernel_size=7, padding=0),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True)
        )

        #downsampling
        self.downsample1 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.InstanceNorm2d(256),
            nn.ReLU(inplace=True)
        )

        # Resnet Block
        self.resnet_block1 = ResnetBlock(256)
        self.resnet_block2 = ResnetBlock(256)
        self.resnet_block3 = ResnetBlock(256)
        self.resnet_block4 = ResnetBlock(256)
        self.resnet_block5 = ResnetBlock(256)
        self.resnet_block6 = ResnetBlock(256)
        self.resnet_block7 = ResnetBlock(256)
        self.resnet_block8 = ResnetBlock(256)
        self.resnet_block9 = ResnetBlock(256)


        # upsample
        self.upsample = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True)
        )

        self.layer2 = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(64, 3, kernel_size=7),
            nn.Tanh()
        )
  

    def forward(self, x):

        x = self.layer1(x)
        x = self.downsample1(x)
    
        x = self.resnet_block1(x)
        x = self.resnet_block2(x)
        x = self.resnet_block3(x)
        x = self.resnet_block4(x)
        x = self.resnet_block5(x)
        x = self.resnet_block6(x)
        x = self.resnet_block7(x)
        x = self.resnet_block8(x)
        x = self.resnet_block9(x)

        x = self.upsample(x)
        x = self.layer2(x) 
        return x

class ResnetBlock(nn.Module):

    def __init__(self, input_ch):
        super().__init__()
    
        self.res_block = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(input_ch, input_ch, kernel_size=3),
            nn.InstanceNorm2d(input_ch),
            nn.ReLU(inplace=True),
            nn.ReflectionPad2d(1),
            nn.Conv2d(input_ch, input_ch, kernel_size=3),
            nn.InstanceNorm2d(input_ch)
        )
  
    def forward(self, x):
        return x + self.res_block(x)
