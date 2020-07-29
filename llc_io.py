import numpy as np 
from codec import Decoder
from codecfile import compress, extract


def imwrite(ndarray, path):
    out = open(path, 'bw')
    out.write(compress(ndarray))
    out.close()
    
def imread(path):
    dec = Decoder(path)
    ndarray = dec.decode()
    return ndarray