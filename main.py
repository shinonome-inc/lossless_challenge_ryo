from utils import mnist_reader
from map_libraly import encode
import numpy as np
from codec import Encoder
from codec import Decoder
from sys import argv

X_train, y_train = mnist_reader.load_mnist('data/fashion', kind='train')
X_test, y_test = mnist_reader.load_mnist('data/fashion', kind='t10k')

data = X_train[50000:50001]

#data2 = [[d for d in dd if d != 0] for dd in data]

data2 = [np.array(dd).reshape([1, -1]) for dd in data]

bpp = []

for i in data2:
    enc = Encoder(i, 'aaa')
    bpp.append(enc.encode())

print(np.average(bpp))


dec = Decoder('aaa', 'bbb.png')
dec.decode()


# from collections import Counter
# import carryless_rangecoder as rc
# from io import BytesIO
#
# # data = list(map(ord, 'qawsedrft4r3gew432rfgyhujikolp;'))
#
# count = [1] * 256
# for i, c in Counter(data).items():
#     count[i] += c
# count_cum = [0] * 256
# for i in range(1, 256):
#     count_cum[i] = count[i] + count_cum[i - 1]
#
# out = BytesIO()
# # Encode
# with rc.Encoder(out) as enc:  # or enc.finish()
#     for index in data:
#         enc.encode(count, count_cum, index)
# # Decode
# decoded = []
# with rc.Decoder(out) as dec:  # or dec.start()
#     for _ in range(len(data)):
#         decoded.append(dec.decode(count, count_cum))
#
# print(data)
# print(decoded)
#
# assert decoded == data
