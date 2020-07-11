import heapq as hq


class HahumanEncode:
    def __init__(self, li: list):
        self.hahuman_list = li
        self.hahuman = {}

    def hahumancoding(self):
        dic = {}
        for tmp in self.hahuman_list:
            if tmp in dic:
                dic[tmp] += 1
            else:
                dic[tmp] = 1
        print("dictionary : {}".format(dic))
        h = []
        for tmp in dic.items():
            hq.heappush(h, [tmp[1], str(tmp[0])])
        print(h)
        while True:
            a = hq.heappop(h)
            b = hq.heappop(h)
            if len(a[1]) < len(b[1]):
                a, b = b, a
            hq.heappush(h, [a[0]+b[0], [a[1], b[1]]])
            if len(h) == 1:
                break
        print(h)
        # hahuman_tree = h[0][1]
        # print("tree : {}".format(hahuman_tree))
        # self.hahuman = coding(hahuman_tree, "")
        return self.hahuman

    # def coding(self, degistr):
    #     for i, small_lst in enumerate(self):
    #         if type(small_list) == str:
    #             hahuman_dic[small_list] = degistr + str(i)
    #         elif i == 0:
    #             small_list.coding(degistr + "0")
    #         else:
    #             small_list.coding(degistr + "1")