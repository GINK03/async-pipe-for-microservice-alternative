import torch
import torch.nn as nn

import numpy as np
import sys
import os
import io
import json
k = ["\n", " ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "]", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "|", "}", "~"]
ci = {k0:i for i, k0 in enumerate(k)}

model = torch.load('model.pt')

def predict(input_line):
    device = torch.device('cpu')
    x = np.zeros((len(input_line), len(ci)+1))
    for i, ch in enumerate(input_line):
        x[i, ci[ch]] = 1
    x = torch.tensor(x, device=device).float()
    y_pred = model(x)

    result = ''
    for ye in y_pred.tolist():
        idx = np.argmax(ye)
        result += k[idx]
    return result

if __name__ == '__main__':
    #line = 'ifmmp xpsme?'
    #predict(line)
    fd_in = sys.stdin.fileno()
    fd_out = sys.stdout.fileno()
    buff = b''
    while True:
        tmp = os.read(fd_in,1)
        if not tmp:
            break
        if tmp != bytes('\n', 'utf8'):
            buff += tmp
        else:
            # 推論
            y_pred = predict(buff.decode('utf8', 'ignore'))
            for ch in y_pred:
                os.write(fd_out, bytes(ch, 'utf8'))
                sys.stdout.flush()
            os.write(fd_out, bytes('\n', 'utf8'))
            sys.stdout.flush()
            os.sync()
            # clear buff
            buff = b''
