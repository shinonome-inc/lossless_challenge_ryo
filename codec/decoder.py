import carryless_rangecoder as cr
from io import BytesIO
from imageio import imwrite, imread
import numpy as np
from .common import _CodecBase
from .common import BYTES_FLAG
from .common import BYTES_FILTER
from .common import BYTES_MAP
from .helper import runlength_decode
from .filter import filter_decode 
from .scanner import map_decode


class Decoder(_CodecBase):
    def __init__(self, input):
        super(Decoder, self).__init__()
        self.stream = BytesIO(open(input, 'rb').read())

        self.algorithm_identify = int.from_bytes(self.stream.read(BYTES_FLAG), 'big')
        self._filter_id = int.from_bytes(self.stream.read(BYTES_FILTER), 'big')
        self._map_id = int.from_bytes(self.stream.read(BYTES_MAP), 'big')
        self._image = np.empty((self._height, self._width), np.uint8)

        self._decoder = cr.Decoder(self.stream)
        self.stream.seek(BYTES_FLAG + BYTES_FILTER + BYTES_MAP)

    def _decode_per_pixel(self):
        return self._decoder.decode(
            self._histogram.tolist(),
            self._histogram_cumulative.tolist()
        )

    def decode(self):
        print("height: {}, width: {}".format(self._height, self._width))
        print("Filter: {}, map: {}".format(self._filter_id, self._map_id))
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
