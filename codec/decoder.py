import carryless_rangecoder as cr
from io import BytesIO
from imageio import imwrite, imread
import numpy as np
import pickle
from .common import _CodecBase
from .common import MAGIC_NUMBER
from .common import BYTES_M
from .common import BYTES_H
from .common import BYTES_W
from .common import BYTES_FILTER
from .common import BYTES_MAP
from .common import FLAG_HUF, FLAG_RNG, BYTES_FLAG, BYTES_DICT
from .common import IMG_H, IMG_W
from .helper import runlength_decode, from_dict
from .filter import filter_decode 
from .scanner import map_decode
from .huffman import HuffmanCoding, Node



class Decoder(_CodecBase):
    def __init__(self, input):
        super(Decoder, self).__init__()
        self.stream = BytesIO(open(input, 'rb').read())

        # assert int.from_bytes(self.stream.read(BYTES_M), 'big') == MAGIC_NUMBER
        self._flag = int.from_bytes(self.stream.read(BYTES_FLAG), 'big')
        self._filter_id = int.from_bytes(self.stream.read(BYTES_FILTER), 'big')
        self._map_id = int.from_bytes(self.stream.read(BYTES_MAP), 'big')
        self._dict_id = int.from_bytes(self.stream.read(BYTES_DICT), 'big')
        self._image = np.empty((IMG_H, IMG_W), np.uint8)

        self._decoder = cr.Decoder(self.stream)
        self.stream.seek(BYTES_FLAG + BYTES_FILTER + BYTES_MAP + BYTES_DICT)


    def _decode_per_pixel(self):
        return self._decoder.decode(
            self._histogram.tolist(),
            self._histogram_cumulative.tolist()
        )
    
    
    def _decode_huffman(self):
        # load data 
        with open("codec/pickles/dicts.pkl", "rb") as f:
            dicts = pickle.load(f)

        code = dicts[self._dict_id]
        int_data = list(memoryview(self.stream.read()))

        # Back to binary array
        bin_s = ""
        for i in range(len(int_data)):
            if i == len(int_data)-2:
                continue
            
            if i == len(int_data)-1:
                rec_8 = format(int_data[i], '08b')
                bin_s += rec_8[-1*int_data[i-1]:]
                break

            bin_s += format(int_data[i], '08b')
        
        # Decode
        rle_decoded = from_dict(code, bin_s)

        return rle_decoded
        
        
    def decode(self):
        print("Filter: {}, map: {}".format(self._filter_id, self._map_id))

        data = None
        if self._flag == FLAG_HUF:
            data = self._decode_huffman()
        
        else:
            data = []
            self._decoder.start()

            for y in range(self._height):
                for x in range(self._width):
                    value = self._decode_per_pixel()
                    self._update_histogram(value)
                    data.append(value)

        rle_decoded = runlength_decode(data)
        map_decoded = map_decode(rle_decoded, self._map_id)
        ft_decoded = filter_decode(map_decoded, self._filter_id)

        return ft_decoded
