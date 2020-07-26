import numpy as np

def filter_encode(img, fid):
    """
    Applies filter to given image

    Parameters:
        img: np.ndarray
            Input image
        fid: int
            kind of filter to apply
    
    Returns:
        out: np.ndarray

    ------------------------------------------
    Filter fids:
        0: None -> Do not apply any filter
        1: Sub -> Row wise
        2: Up -> Column wise
        3: Avg -> Average filter
    """
    out = img.copy()
    H, W = img.shape

    # Sub
    if fid ==1:
        for h in range(H):
            for w in range(1, W):
                out[h, w] = img[h, w] - img[h, w-1]
    # Up
    elif fid == 2:
        for h in range(1, H):
            for w in range(W):
                out[h, w] = img[h, w] - img[h-1, w]
    # Average
    elif fid == 3:
        for h in range(1, H):
            for w in range(1, W):
                out[h, w] = img[h, w] - (img[h, w-1] + img[h-1, w]) // 2
    

    return out

def filter_decode(img, fid):
    """
    Decodes filter of given image

    Parameters:
        img: np.ndarray(dtype=uint8)
            filtered image
        fid: int
            kind of filter to decode
    
    Returns:
        out: np.ndarray

    ------------------------------------------
    Filter fids:
        0: None -> Do not apply any filter
        1: Sub -> Row wise
        2: Up -> Column wise
        3: Avg -> Average filter
    """
    out = img.copy()
    H, W = img.shape

    if fid == 1:
        for h in range(H):
            for w in range(1, W):
                out[h, w] = out[h, w] + out[h, w-1]
    
    elif fid == 2:
        for h in range(1, H):
            for w in range(W):
                out[h, w] = out[h, w] + out[h-1, w]
    
    elif fid == 3:
        for h in range(1, H):
            for w in range(1, W):
                out[h, w] = out[h, w] + (out[h, w-1] + out[h-1, w]) // 2
    

    return out

class Filter(object):
    """
        このクラスでは，  フィルターを実装しています。
    """
    def __init__(self, data):
        self.data = data


    def sub(self):
        data_filtered = np.zeros((28, 28), dtype = np.uint8)
        for raw in range(28):
            for column in range(28):
                if column == 0:
                    data_filtered[raw, column] = self.data[raw, column]
                else:
                    data_filtered[raw, column] = self.data[raw, column] - self.data[raw, column - 1]
        return data_filtered


    def sub_decode(self) :
        data_original = np.zeros((28, 28), dtype = np.uint8)
        for raw in range(28) :
            for column in range(28) :
                if column == 0 :
                    data_original[raw, column] = self.data[raw, column]
                else :
                    data_original[raw, column] = self.data[raw, column] + data_original[raw, column - 1]
        return data_original

    def up(self):
        data_filtered = np.zeros((28, 28), dtype = np.uint8)
        for raw in range(28):
            for column in range(28):
                if raw == 0:
                    data_filtered[raw, column] = self.data[raw, column]
                else:
                    data_filtered[raw, column] = self.data[raw, column] - self.data[raw - 1, column]
        return data_filtered


    def up_decode(self):
        data_original = np.zeros((28, 28), dtype = np.uint8)
        for raw in range(28):
            for column in range(28):
                if raw == 0:
                    data_original[raw, column] = self.data[raw, column]
                else:
                    data_original[raw, column] = data_original[raw - 1, column] + self.data[raw, column]
        return data_original


    def average(self):
        data_filtered = np.zeros((28, 28), dtype = np.uint8)
        for raw in range(28):
            for column in range(28):
                if raw == 0 or column == 0:
                    data_filtered[raw, column] = self.data[raw, column]
                else:
                    data_filtered[raw, column] = self.data[raw, column] - ((self.data[raw, column-1] + self.data[raw - 1, column]) // 2)
        return data_filtered


    def average_decode(self):
        data_original = np.zeros((28, 28), dtype = np.uint8)
        for raw in range(28):
            for column in range(28):
                if raw == 0 or column == 0:
                    data_original[raw, column] = self.data[raw, column]
                else:
                    data_original[raw, column] = self.data[raw, column] + ((data_original[raw, column-1] + data_original[raw - 1, column]) // 2)
        return data_original


    def peathcalculate(self, left, diagonal, above):
        """
        peath値を計算する関数です。

        Parameters
        ----------
        left, diagonal, above : int
        それぞれ目標の画素の左隣，左斜め上，真上の画素の値を想定しています。

        See Also
        --------
        horizon , vertical , sum : int
        それぞれ水平方向の変化量，垂直方向の変化量，およびそれらの和を示します。
        """
        horizon = abs(above - diagonal)
        vertical = abs(left - diagonal)
        sum = abs(above - diagonal + left - diagonal)
        if horizon <= vertical and horizon <= sum:
            self.peath = left
        if vertical <= sum:
            self.peath = above
        else:
            self.peath = diagonal


    def peath(self):
        data_filtered = np.zeros((28, 28), dtype = np.uint8)
        for raw in range(28) :
            for column in range(28) :
                if raw == 0 or column == 0 :
                    data_filtered[raw, column] = self.data[raw, column]
                else:
                    self.peathcalculate(self.data[raw, column - 1], self.data[raw - 1, column - 1], self.data[raw - 1, column])
                    data_filtered[raw, column] = self.data[raw, column] - self.peath
        return data_filtered


    def peath_decode(self):
        data_original = np.zeros((28, 28), dtype = np.uint8)
        for raw in range(28) :
            for column in range(28) :
                if raw == 0 or column == 0 :
                    data_original[raw, column] = self.data[raw, column]
                else:
                    self.peathcalculate(data_original[raw, column - 1], data_original[raw - 1, column - 1], data_original[raw - 1, column])
                    data_original[raw, column] = self.data[raw, column] + self.peath
        return data_original
