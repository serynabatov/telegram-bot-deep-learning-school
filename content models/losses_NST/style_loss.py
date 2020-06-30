import torch
from gram import GramMatrix
import torch.nn as nn

class StyleLoss(nn.Module):

    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        gram = GramMatrix(target_feature.detach())
        self.target = gram.calculate()

    def forward(self, input):
        G = GramMatrix(input)
        target_G = G.calculate()
        self.loss = torch.nn.functional.mse_loss(target_G, self.target)
        return input

