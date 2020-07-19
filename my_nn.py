from torch import nn, optim
import torch.nn.functional as F

class Net_2hl(nn.Module):
    def __init__(self, n_features, n_hl1, n_hl2):
        super(Net_2hl, self).__init__()
        self.hl1 = nn.Linear(n_features, n_hl1)
        self.hl2 = nn.Linear(n_hl1, n_hl2)
        self.output_layer = nn.Linear(n_hl2, 3) #Tres possiveis saidas: classificação
        # em positivo, negativo ou indeterminado

    def forward(self, x):
        h1 = F.relu(self.hl1(x))
        h2 = F.relu(self.hl2(h1))
        y = F.sigmoid(self.output_layer(h2))

        return y