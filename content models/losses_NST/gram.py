import torch

class GramMatrix():

    def __init__(self, input):
        self.input = input
        self.batch_size, self.number_of_feature_maps, self.height, self.width = input.size()

    def calculate(self):
        features = self.input.view(self.batch_size * self.number_of_feature_maps, self.height * self.width)

        G = torch.mm(features, features.t())  
        # Нормализуем величины
        return G.div(self.batch_size * self.number_of_feature_maps * self.height * self.width)  
