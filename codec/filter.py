def sub_filter(self):
    """Sub：２列目以降のピクセル値を左のピクセル値との差で置き換える"""
    lst = self._imgfilter
    sub = [0] * self._width
    for y in range(self._height):
        for x in range(self._width - 1, 0, -1):
            sub[x] = lst[y][x] - lst[y][x-1]
            lst[y][x] = sub[x] % 256
    return lst


def up_filter(self):
    """Up：二行目以降のピクセル値を真上のピクセル値との差で置き換える"""
    lst = self._imgfilter
    up = [0] * self._width
    print(lst[254])
    print(lst[255])
    for y in range(self._height-1, 0, -1):
        for x in range(self._width):
            up[x] = lst[y][x] - lst[y-1][x]
            lst[y][x] = up[x] % 256
    return lst
