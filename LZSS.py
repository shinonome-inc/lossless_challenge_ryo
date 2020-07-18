def lzss(data):
    """
        LZSS圧縮を実装した関数です。のちにハフマン符号化とあわせてclass Deflateとします。

        Parameters
        ----------
        data : list
            画像の画素の一次元配列を想定しています。

        Returns
        -------
        data_lzss : list
            lzss圧縮後の画素の値の一次元配列を想定しています。のちにハフマン符号化もします。

        See Also
        --------
        data_reference : list
        現在読み込んでいる画素より前の画素によるlistです。
        ここに現在読み込んでいる画素のパターンがあれば，置き換えて圧縮します。

        matchindexes　:　list
        現在読み込んでいる画素と一致する画素のdata_referenceにおけるインデックスmatchindexが集まったリストです。
        ３つ以上一致しないものは圧縮を行わないため省き，３つ以上一致するものは
        その一致している長さlengthをkeyとした辞書 matchindexes_and_lengthに入れて，
        その中からlengthが最大のものの位置（256以上）とlengthをdata_lzssに追加します。

        54~59行目のif文は画素のデータの圧縮が画素の最後の要素まで行われる時のためのものです。

        """


    data_reference = []
    data_lzss = [data[0]]
    index = 1
    while index < len(data):
        data_reference.append(data[index-1])
        if data[index] in data_reference and index < len(data) - 2\
                                         and len(data_reference) > 3:
            matchindexes = [i for i, x in enumerate(data_reference)\
                            if x == data[index]]
            matchindexes_and_length = {}
            for matchindex in matchindexes:
                if data[index + 1] != data_reference[matchindex + 1] or \
                        data[index + 2] != data_reference[matchindex + 2]:
                    matchindexes.remove(matchindex)
                    continue
                distance = index - matchindex
                length = 0
                while data_reference[matchindex] == data[matchindex + distance] \
                        and matchindex < len(data_reference) - 1 \
                        and matchindex + distance < len(data) - 1 :
                    length += 1
                    matchindex += 1
                    if data_reference[matchindex] == data[matchindex + distance] and\
                            (matchindex == len(data_reference) - 1 or \
                        matchindex + distance == len(data) - 1):
                        length +=1
                        matchindex += 1
                        break
                matchindex -= length
                matchindexes_and_length[length] = matchindex
            if matchindexes_and_length:
                data_lzss.append(255 + index - matchindexes_and_length[max(matchindexes_and_length.keys())])
                data_lzss.append(max(matchindexes_and_length.keys()))
                index += length
            else:
                data_lzss.append(data[index])
                index += 1
        else:
            data_lzss.append(data[index])
            index += 1
    return data_lzss