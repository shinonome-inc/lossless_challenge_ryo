import numpy as np 
import matplotlib.pyplot as plt


def map_encode(img, map_id):
    out = img.copy()

    if map_id == 1:
        return column_wise_encode(out)
    
    return list(img.ravel())

def map_decode(arr, map_id):
    H, W = 28, 28

    if map_id == 1:
        return column_wise_decode(arr)
    
    out = np.array(arr).reshape(H, W).astype(np.uint8)
    return out

    
def column_wise_encode(img):
    """
    Scan the given image column wise (left to  right) and expand pixel values to 1d array

    Parameters:
        img: np.ndarray
            Given image
    
    Returns:
        out: list
            Scanned pixel values

    ------------------------
    map_id:
        0 => None
        1 => Column wise
    """
    H, W = img.shape
    out = []
    
    for w in range(W):
        for h in range(H):
            out.append(img[h, w])
    
    return out

def column_wise_decode(arr):
    """
    Decoder for column_wise_encode

    Parameters:
        arr: list || np.array
            array of pixel values
    
    Returns:
        img: np.ndarray
            Given image
    """
    H, W = 28, 28
    
    # plt.figure(1)
    # plt.imshow(np.array(arr).reshape(H, W))
    # plt.show()

    img = np.array(arr).reshape(H, W).astype(np.uint8).T
    return img
