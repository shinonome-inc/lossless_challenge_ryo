def sub_filter(array, height, width):
    """Apply a sub_filter.

    Parameters
    ----------
    array: ndarray
    height: int
    width: int

    """
    for y in range(height):
        for x in range(width - 1, 0, -1):
            array[y][x] = int(array[y][x]) - int(array[y][x-1])
    return array


def up_filter(array, height, width):
    """Apply a up_filter.

    Parameters
    ----------
    array: ndarray
    height: int
    width: int

    """
    for y in range(height-1, 0, -1):
        for x in range(width):
            array[y][x] = int(array[y][x]) - int(array[y-1][x])
    return array
