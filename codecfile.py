import numpy as np
import multiprocessing as multi
from multiprocessing import Pool

from codec import Encoder

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

    enc = Encoder(img, filter_id)

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
    list_of_combinations = []

    n_cores = multi.cpu_count()
    with Pool(n_cores) as p:
        results = p.map(func=encode, args=list_of_combinations)
    
    best = results[np.argmax(results)]

    return best

def extract(img):
    pass