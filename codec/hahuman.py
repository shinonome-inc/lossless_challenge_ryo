import heapq as hq


class HahumanEncode:
    def __init__(self, li: list):
        self.hahuman_list = li

    def hahuman_tree(self):
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
        print("h" + str(type(h)))
        print(h)
        while True:
            a = hq.heappop(h)
            b = hq.heappop(h)
            print(a[1], b[1])
            if len(a[1]) < len(b[1]):
                a, b = b, a
            hq.heappush(h, [a[0]+b[0], [a[1], b[1]]])
            if len(h) == 1:
                break
        hahuman_tree = h[0][1]
        print("tree : {}".format(hahuman_tree))
        return hahuman_tree

    # def coding(hahuman_tree, degistr):
    #     hahuman = {}
    #     for i, small_lst in enumerate(lst):
    #         if type(small_lst) == str:
    #             hahuman[small_lst] = degistr + str(i)
    #         elif i == 0:
    #             coding(small_lst, degistr + "0")
    #         else:
    #             coding(small_lst, degistr + "1")