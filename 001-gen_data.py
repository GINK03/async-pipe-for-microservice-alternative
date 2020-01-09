import numpy as np
from itertools import count
import random
import numpy as np
import json
#for i in range(12354, 12588+1):

shakespeare = open('./shakespeare.txt').read().replace('\ufeff', '')
k = sorted(set(list(shakespeare)))
print('char-list', json.dumps(k, ensure_ascii=False))

v = k[1:] + [k[0]]
# vk is for decryption
vk = {v0:k0 for k0,v0 in zip(k,v)}
# kv is for cryption
kv = {k0:v0 for k0,v0 in zip(k,v)}

# for one-hot encoding, dict
ci = {k0:i for i, k0 in enumerate(k)}

# example cryption.
for c in 'hello world!':
    print(kv[c], end='')
print()
# example cryption2.
crypt = ''.join([kv[c] for c in shakespeare])
with open('./crypt_shakespear.txt', 'w') as fp:
    fp.write(crypt)


x = np.zeros((10**6, len(vk)+1))
y = np.zeros((10**6, len(vk)+1))
for i in range(len(x)):
    vc = random.choice(v)
    kc = vk[vc]
    #print(vc, kc)
    vi, ki = map(lambda x:ci[x], [vc, kc])

    x[i, vi] = 1
    y[i, ki] = 1

np.savez_compressed('data', x=x, y=y)
