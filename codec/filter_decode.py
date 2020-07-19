import numpy as np
class Filter_decode(object):
    """
        このクラスでは，  フィルターのデコードを実装しています。
        差を取るフィルターに関しては，フィルター処理によってマイナスになることはない（-1 = 254, -2 = 253・・・とするため）ので，255による剰余をとります。
    """
    def __init__(self, data):
        self.data = data
        self.peath == 0


    def none_decode(self, data):
        return self.data


    def sub_decode(self):
        data_original_raw = []
        raw = 0
        while raw < 28:
            for i in range(28):
                if i == 0:
                    data_original_raw.append(self.data[raw, i])
                else:
                    data_original_raw.append((self.data[raw, i] + self.data[raw, i-1]) % 255)
        self.data[raw] = np.array(data_original_raw)
        raw += 1
        return self.data


    def up_decode(self):
        data_original_raw = []
        raw = 1
        while raw < 28:
            for i in range(28):
               data_original_raw.append((self.data[raw - 1, i] + self.data[raw, i]) % 255)
        self.data[raw] = np.array(data_original_raw)
        raw += 1
        return self.data


    def average_decode(self):
        data_original_raw = []
        raw = 1
        while raw < 28:
            for i in range(28):
                if i == 0:
                    data_original_raw.append(self.data[raw, i])
                else:
                    data_original_raw.append((self.data[raw, i] + ((self.data[raw, i-1] + self.data[raw - 1, i]) // 2)) % 255)
        self.data[raw] = np.array(data_original_raw)
        raw += 1
        return self.data

    def peath(self, left, diagonal, above):
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
            self.peath = int(left)
        if vertical <= sum:
            self.peath = int(above)
        else:
            self.peath = (diagonal)


    def peath_decode(self):
        data_original_raw = []
        raw = 1
        while raw < 28:
            for i in range(28):
                if i == 0:
                    data_original_raw.append(self.data[raw, i])
                else :
                    self.peath(self.data[raw, i - 1], self.data[raw - 1, i - 1], self.data[raw - 1, i])
                    data_original_raw.append((self.data[raw, i] + self.peath()) % 255)
        self.data[raw] = np.array(data_original_raw)
        raw += 1
        return self.data













