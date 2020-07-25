import numpy as np 
from codecfile import compress, extract
​
def imwrite(ndarray, path):
    out = open(path, 'bw')
    out.write(compress(ndarray))
    out.close()
​
def imread(path):
    ndarray = np.fromfile(path, dtype=np.uint8)
    return extract(ndarray)