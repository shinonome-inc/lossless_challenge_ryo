def sub_filter(self):
    """Sub：２列目以降のピクセル値を左のピクセル値との差で置き換える"""
    sub = [0] * self.width
    for y in range(self._height): 
        for x in range(1, self.width):
            sub[x] = self._image[y][0] - self._image[y][x]
            self._image[y][x] = (sub[x] + self._image[y][x]) % 256


def up_filter(self):
    """Up：二行目以降のピクセル値を真上のピクセル値との差で置き換える"""
    up = [0] * self.width
    for y in range(1, self.height):
        for x in range(self.width):
            up[x] = self._image[y-1][x] - self._image[y][x]
            self._image[y][x] = (up[x] + self._image[y][x]) % 256