import torch
from torch import nn


class BtcLSTM(nn.Module):
    def __init__(self, num_features, num_hidden, num_layers):
        super(BtcLSTM, self).__init__()

        self.n_layers = num_layers
        self.n_hidden = num_hidden

        self.lstm = nn.LSTM(input_size=num_features, hidden_size=num_hidden, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(num_hidden*30, 1)

    def forward(self, x):
        h0 = torch.zeros(self.n_layers, x.size(0), self.n_hidden)
        c0 = torch.zeros(self.n_layers, x.size(0), self.n_hidden)

        out, (hs, _) = self.lstm(x, (h0, c0))

        return self.fc(out.contiguous().view(x.size(0), -1))
