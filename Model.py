
import torch
import torch.nn as nn

class Model(torch.nn.Module):
    def __init__(self, D_in, D_out):
        super(Model, self).__init__()
        self.l1 = torch.nn.Linear(D_in, 1000)
        self.l2s = [torch.nn.Linear(1000, 1000) for i in range(5)]
        self.l3 = torch.nn.Linear(1000, D_out)
        self.optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        self.criterion = nn.BCELoss()

    def forward(self, x):
        h = self.l1(x)
        for i in range(3):
            h = self.l2s[i](h).clamp(min=0)
        y_pred = nn.Sigmoid()(self.l3(h))
        return y_pred

    def train_batch(self, y_pred, y, step=0):
        loss = self.criterion(y_pred, y)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        print(step, loss.tolist())
