import carryless_rangecoder as cr
import numpy as np
import pickle
from io import BytesIO
from imageio import imread
from .common import _CodecBase
from .common import MAGIC_NUMBER
from .common import BYTES_M
from .common import BYTES_H
from .common import BYTES_W
from .common import BYTES_FILTER
from .common import BYTES_MAP
from .filter import filter_encode
from .helper import runlength_encode, to_freq_vector
from .scanner import map_encode
from .huffman import HuffmanCoding


class Encoder(_CodecBase):
    def __init__(self, input, filter_id, map_id):
        super(Encoder, self).__init__()
        self._stream = BytesIO()
        self._stream_huff = BytesIO()
        self._image = input
        self._filter_id = int(filter_id)
        self._map_id = int(map_id)
        self._height, self._width = self._image.shape

        # Rangecoder
        self._stream.write(MAGIC_NUMBER.to_bytes(BYTES_M, 'big'))
        self._stream.write(self._width.to_bytes(BYTES_W, 'big'))
        self._stream.write(self._height.to_bytes(BYTES_H, 'big'))
        self._stream.write(self._filter_id.to_bytes(BYTES_FILTER, 'big'))
        self._stream.write(self._map_id.to_bytes(BYTES_MAP, 'big'))

        # Huffman
        self._stream_huff.write(MAGIC_NUMBER.to_bytes(BYTES_M, 'big'))
        self._stream_huff.write(self._width.to_bytes(BYTES_W, 'big'))
        self._stream_huff.write(self._height.to_bytes(BYTES_H, 'big'))
        self._stream_huff.write(self._filter_id.to_bytes(BYTES_FILTER, 'big'))
        self._stream_huff.write(self._map_id.to_bytes(BYTES_MAP, 'big'))

        self._encoder = cr.Encoder(self._stream)


    def _encode_per_pixel(self, value):
        self._encoder.encode(
            self._histogram.tolist(),
            self._histogram_cumulative.tolist(),
            value
        )
    

    def _encode_huffman(self, data):
        # Load data
        with open("codec/pickles/cluster_centers.pkl", "rb") as f:
            cluster_centers = pickle.load(f)
        with open("codec/pickles/dicts.pkl", "rb") as f:
            dicts = pickle.load(f)
        
        # Determine label
        freq = to_freq_vector(data)
        label = np.argmin(np.apply_along_axis(lambda x: np.linalg.norm(freq-x), 1, cluster_centers))
        # Encoding
        huff = HuffmanCoding()
        huff.code = dicts[label]
        encoded = huff.encode(data)

        print(encoded, len(encoded)*8 / (784))

        # Write 
        last_len = len(encoded) % 8
        int_list = list(int(encoded[i : i + 8], 2) for i in range(0, len(encoded), 8))
        for i in range(len(int_list)):
            if i == len(int_list)-1:
                self._stream_huff.write(last_len.to_bytes(1, "big"))
            
            self._stream_huff.write(int_list[i].to_bytes(1, "big"))


    def encode(self):
        # Filter + map + runlength
        img_filtered = filter_encode(self._image, self._filter_id)
        img_scanned = map_encode(img_filtered, self._map_id)
        data = runlength_encode(img_scanned)

        # Huffman
        self._encode_huffman(data.copy())
        huff_encoded = self._stream_huff.getvalue()

        # Rangecoder
        for value in data:
            self._encode_per_pixel(value)
            self._update_histogram(value)

        # Default 
        # for y in range(self._height):
        #     for x in range(self._width):
        #         value = self._image[y, x]
        #         self._encode_per_pixel(value)
        #         self._update_histogram(value)

        self._encoder.finish()
        encoded = self._stream.getvalue()

        print("")
        print("HUFFMAN: {}".format(len(huff_encoded)*8 / 784))
        print("RANGE: {}".format(len(encoded) * 8 / 784))

        return encoded

