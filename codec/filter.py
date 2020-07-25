import numpy as np



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
