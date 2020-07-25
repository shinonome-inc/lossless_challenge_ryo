import numpy as np


def sub_filter(array, height, width):
    """Apply a sub_filter.

    Parameters
    ----------
    array: ndarray
        array for filtering
    height: int
        height of array
    width: int
        width of array

    Returns
    -------
    filter: ndarray
        filtered array
    """
    filter = [[array[i][0] for j in range(width)] for i in range(height)]
    filter = np.array(filter, dtype='uint')
    for y in range(height):
        for x in range(1, width):
            filter[y][x] = array[y][x] - array[y][x-1]
    return filter


def up_filter(array, height, width):
    """Apply a up_filter.

    Parameters
    ----------
    array: ndarray
        array for filtering
    height: int
        height of array
    width: int
        width of array

    Returns
    -------
    filter: ndarray
        filtered array
    """
    filter = [[array[i][0] for j in range(width)] for i in range(height)]
    filter = np.array(filter, dtype='uint')
    for y in range(1, height):
        for x in range(width):
            filter[y][x] = array[y][x] - array[y-1][x]
    return filter
