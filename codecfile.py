import numpy as np
import multiprocessing as multi
from multiprocessing import Pool

from codec import Encoder
from codec.common import NUM_FILTER
from codec.common import NUM_MAP

def encode(cmb):
    """
    Driver function for compress()


    ----------------
    Parameters:
        cmb: list => [img, filter_id, map_id]
    
    Returns:
        encoded: bytes
            Encoded file (header info + img)

    """
    img, filter_id, map_id = cmb
    print(filter_id, map_id)
    enc = Encoder(img, filter_id, map_id)
    return enc.encode()
    

def compress(img):
    """
    Try combinatios of MAPs and filers on input image and return the best result

    --------------------
    Parameters:
        img: np.ndarray
            input image (Fashion-MNIST test images)
    
    Returns:
        best: bytes
            Compressed image with shortest length among all trials

    """
    combinations = [(img.copy(), i, j) for i in range(NUM_FILTER) for j in range(NUM_MAP)]

    n_cores = multi.cpu_count()
    with Pool(n_cores) as p:
        results = p.map(encode, combinations)
    
    print(results)
    best = results[np.argmin(list(map(len, results)))]

    return best

def extract(img):
    pass