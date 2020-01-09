import torch
import torch.nn as nn
import numpy as np
from tqdm import tqdm
from Model import Model

device = torch.device('cpu')

npz = np.load('./data.npz')
x,y = npz['x'], npz['y']
x = torch.tensor(x, device=device).float()
y = torch.tensor(y, device=device).float()
size = x.shape[1]
model = Model(D_in=size, D_out=size)
for epoch in range(0, 1):
    B = 64
    for b in tqdm(range(0, len(x), B)):
        y_pred = model(x[b:b+B])
        model.train_batch(y_pred, y[b:b+B], epoch)
    torch.save(model, 'model.pt')
    # 1 epochでいい
