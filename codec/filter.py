import numpy as np

filter = np.zeros((256, 256), dtype='uint')


def sub_filter(array, height, width):
    """Apply a sub_filter.

    Parameters
    ----------
    array: ndarray
    height: int
    width: int

    """
    for y in range(height):
        for x in range(1, width):
            filter[y][x] = array[y][x] - array[y][x-1]
    return filter


def up_filter(array, height, width):
    """Apply a up_filter.

    Parameters
    ----------
    array: ndarray
    height: int
    width: int

    """
    for y in range(1, height):
        for x in range(width):
            filter[y][x] = array[y][x] - array[y-1][x]
    return filter
