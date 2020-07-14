"""
このモジュールではpngにおける前処理，つまりフィルターを実装しています。
"""

import numpy as np
class Png_filter(object):
    """
       このクラスでは，pngにおける前処理，つまりフィルターによる処理を実装しています。
    """

    def __init__(self, data):
        """
                         入力された画素のデータをself.dataとして，どのフィルターにも持たせます


                        Args:
                        　　　　　data(numpy.ndarray): 画像ごとの画素のデータです。28*28の大きさになります。
        """
        self.data = data


    def none_filter(self):
        """　　
        何もしない場合のフィルターです。行によっては何の処理もする必要がない場合があるので，その際はこの関数を実行します。
        """
        return self.data






    def sub_filter(self):
        """
            左隣の画素の値との差を画素として用いるsubフィルターを実装した関数です。行ごとにforループを回し，
            処理後の画素の値を持つリストをdata_filtered_rowとして作成し，ループが終わったら元のデータ行を置き換えます。
             フィルターの使用上左端の画素は変更しないので，各行のi==0の場合は特別扱いしています。
                Returns:
                   subフィルターによって前処理された画素のデータをnumpy.ndarray型で返します。

        """
        data_filtered_row = []
        row = 0
        while row < 28:
            for i in range(28):
                if i == 0:
                    data_filtered_row.append(self.data[row, i])
                else:
                    data_filtered_row.append(self.data[row, i] - self.data[row, i-1])
            self.data[row] = np.array(data_filtered_row)
            data_filtered_row = []
            row += 1
        return self.data


    def up_filter(self):
        """
        　　　真上の画素の値との差を画素として用いるupフィルターを実装した関数です。行ごとにforループを回し，
            処理後の画素の値を持つリストをdata_filtered_rowとして作成し，ループが終わったら元のデータ行を置き換えます。
　　　　　　　　　フィルターの仕様上，最も上の行（0行目）の画素は変更しないので，row>=1として処理しています。
            Returns:
                subフィルターによって前処理された画素のデータをnumpy.ndarray型で返します。

        """
        data_filtered_row = []
        row = 1
        while row < 28:
            for i in range(28):
               data_filtered_row.append(self.data[row-1, i] - self.data[row, i])
            self.data[row] = np.array(data_filtered_row)
            data_filtered_row = []
            row += 1
        return self.data






