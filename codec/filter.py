def sub_filter(array, height, width):
    """Sub：２列目以降のピクセル値を左のピクセル値との差で置き換える"""
    for y in range(height):
        for x in range(width - 1, 0, -1):
            array[y][x] = int(array[y][x]) - int(array[y][x-1])
    return array


def up_filter(array, height, width):
    """Up：二行目以降のピクセル値を真上のピクセル値との差で置き換える"""
    for y in range(height-1, 0, -1):
        for x in range(width):
            array[y][x] = int(array[y][x]) - int(array[y-1][x])
    return array
