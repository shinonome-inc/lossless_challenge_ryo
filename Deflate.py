from collections import Counter
import heapq
class Deflate(object):
    """
    このモジュールでは，  deflate圧縮を実装しています。
    """


    def lzss_encode(self, data):
        """
                  LZSS圧縮を実装した関数です。

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
            data_reference.append(data[index - 1])
            if data[index] in data_reference and index < len(data) - 2\
                    and len(data_reference) > 3:
                matchindexes = [i for i, x in enumerate(data_reference)\
                                if x == data[index] and i < len(data_reference)-2]
                matchindexes_and_length = {}
                for matchindex in matchindexes :
                    if data[index + 1] != data_reference[matchindex + 1] or\
                            data[index + 2] != data_reference[matchindex + 2]:
                        matchindexes.remove(matchindex)
                        continue
                    distance = index - matchindex
                    length = 0
                    while data_reference[matchindex] == data[matchindex + distance] \
                            and matchindex < len(data_reference) - 1 \
                            and matchindex + distance < len(data) - 1:
                        length += 1
                        matchindex += 1
                        if data_reference[matchindex] == data[matchindex + distance] and\
                                (matchindex == len(data_reference) - 1 or
                                 matchindex + distance == len(data) - 1):
                            length += 1
                            matchindex += 1
                            break
                    matchindex -= length
                    matchindexes_and_length[length] = matchindex
                if matchindexes_and_length:
                    data_lzss.append(255 + index - matchindexes_and_length[max(matchindexes_and_length.keys())])
                    data_lzss.append(max(matchindexes_and_length.keys()))
                    index += length
                else :
                    data_lzss.append(data[index])
                    index += 1
            else :
                data_lzss.append(data[index])
                index += 1
        return data_lzss


    def lzss_decode(self, data):
        data_original = []
        index = 0
        while index < len(data):
            if data[index] > 255:
                position = index - (data[index] - 255)
                length = data[index + 1]
                data_original.extend([bit for bit in data[position : position + length]])
                index += 2
            else:
                data_original.append(data[index])
                index += 1
        return data_original

    def huffman_encode(self, data):
        """　　　　　　　
                          ハフマン符号化を実装した関数です。LZSSによって長さと位置に変換された位置は256以上のデータが出現するので，それを目印に
                          違うハフマン木を作成します。("1"とされているリストや辞書は画素の値，"2"とされているリストや辞書はLZSSによって
                          長さと位置に変換されたものを扱っています。)

                          Parameters
                          ----------
                          data : list
                              画像の画素の一次元配列を想定しています。

                          Returns
                          -------
                          data_huffman : list
                              ハフマン符号化が施された画素の値を一次元配列にて返します。

                          See Also
                          --------
                          最終的にはcodetableという辞書に，元のデータをkey,ハフマン符号化による符号をvalueとして収納します。
                          まず，data1にはLZSSの影響を受けていない画素の値，data2にはLZSSによって変換された位置と長さの値を収納し，
                          それらに含まれる要素をkey,その要素の頻度をvalueとする辞書elements_frequencyを作成します。
                          そしてelements_frequencyのvalueとkeyを同じリストに入れ（value），さらにそのリストを集めたリストをtreeとし，
　　　　　　　　　　　　　 　treeをheapにした後はvalue，すなわち頻度が最小の２つを取り出していき，そのたびに取り出された要素がkeyとなるcodetableのvalueに，
                          ハフマン木の符号となる0または1を加えます。そして取り出された2つの和を取って新たにtreeに加え，最終的にtreeが完成するまで繰り返します。

　　　　　　　　　　　　　　 huffman_switchmark　：　str
                           デコードの際，tree2におけるハフマン木を用いる際は，この 0の羅列を目印にします。
　　　　　　　　　　　　　　　　　　　　
        """
        data1 = []
        data2 = []
        data_huffman = []
        index = 0
        while index < len(data):
            if data[index] <= 255:
                data1.append(data[index])
                index += 1
            else:
                data2.extend([data[index], data[index+1]])
                index += 2
        elements_frequency1 = Counter(data1)
        codetable1 = {k : "" for k in elements_frequency1.keys()}
        tree1 = [[v, [k]] for k, v in elements_frequency1.items()]
        heapq.heapify(tree1)

        elements_frequency2 = Counter(data2)
        codetable2 = {k : "" for k in elements_frequency2.keys()}
        tree2 = [[v, [k]] for k, v in elements_frequency2.items()]
        heapq.heapify(tree2)

        while len(tree1) > 1:
            min_left = heapq.heappop(tree1)
            min_right = heapq.heappop(tree1)
            new = [l + r for l, r in zip(min_left, min_right)]
            heapq.heappush(tree1, new)
            for letter in min_left[1] :
                codetable1[letter] += "0"
            for letter in min_right[1] :
                codetable1[letter] += "1"
        for k, v in codetable1.items() :
            codetable1[k] = v[: :-1]

        while len(tree2) > 1:
            min_left = heapq.heappop(tree2)
            min_right = heapq.heappop(tree2)
            new = [l + r for l, r in zip(min_left, min_right)]
            heapq.heappush(tree2, new)
            for letter in min_left[1] :
                codetable2[letter] += "0"
            for letter in min_right[1] :
                codetable2[letter] += "1"
        for k, v in codetable2.items() :
            codetable2[k] = v[: :-1]

        longestsign = max([len(sign) for sign in codetable1.values()] + [len(sign) for sign in codetable2.values()])
        huffman_switchmark = '0'*(longestsign + 1)

        for bit in data:
            if bit <= 255 :
                data_huffman.append(codetable1[bit])
            else:
                data_huffman.append(huffman_switchmark)
                data_huffman.append(codetable2[bit])
        self.codetable1 = codetable1
        self.codetable2 = codetable2
        self.huffman_switchmark = huffman_switchmark
        return data_huffman

    def huffman_decode(self, data):
        """　　　　　　　
        ハフマン符号化されたデータのデコードを実装した関数ですが，codetableのkeyとvalueを逆にしたdecodetableの部分で
        TypeError: cannot unpack non-iterable int objectとエラーが出てしまいます。
        原因がよく分からないのでレビューお願いします。
        """
        data_original = []
        decodetable1 = {v: k for k, v in self.codetable1}
        decodetable2 = {v: k for k, v in self.codetable2}
        index = 0
        while index < len(data):
            if data[index] == self.huffman_switchmark:
                data_original.append(decodetable2[data[index + 1]])
                data_original.append(decodetable2[data[index + 2]])
                index += 3
            else:
                data_original.append(decodetable1[data[index]])
                index += 1
        return data_original





