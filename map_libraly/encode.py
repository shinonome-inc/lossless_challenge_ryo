import carryless_rangecoder as rc
from io import BytesIO
from io import StringIO
from collections import Counter

class Encode():
    def __init__(self, input_array):
        self.image_array = input_array


    def encode(self):
        out = BytesIO()
        self.count = [1]*256
        for i, c in Counter(self.image_array).items():
            self.count[i] += c
        self.count_cum = [0]*256

        print(self.image_array)

        for i in range(1, 256):
            self.count_cum[i] = self.count[i] + self.count_cum[i - 1]

        with rc.Encoder(out) as enc:
            for index in self.image_array:
                enc.encode(self.count, self.count_cum, index)

        self.out = out

    def decode(self):
        self.decoded = []
        out = self.out
        with rc.Decoder(out) as dec:  # or dec.start()
            for _ in range(784):
                self.decoded.append(dec.decode(self.count, self.count_cum))
