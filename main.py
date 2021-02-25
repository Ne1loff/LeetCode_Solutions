import unittest

shortest_path = 2 ** 32


class Node:
    def __init__(self, red_dst, blue_dst):
        self.red_dst = red_dst
        self.blue_dst = blue_dst


def go(nodes, index, red_edge):
    return go_w_ls_i(nodes, index, -1, red_edge, 0, None)


def go_w_ls_i(nodes, index, last_index, edge_color, loc_s_p, lst_edg):
    global shortest_path

    if len(nodes[index].red_dst) == 0 and len(nodes[index].blue_dst) == 0:
        if loc_s_p == 0:
            if shortest_path == 2 ** 32:
                shortest_path = -1
        else:
            return loc_s_p
    if edge_color and len(nodes[index].red_dst) != 0:
        for r_e in nodes[index].red_dst:
            if r_e[0] == 0:
                if loc_s_p < shortest_path or shortest_path == -1:
                    shortest_path = loc_s_p + 1
                return 1
            else:
                if r_e[0] == last_index and index != last_index:
                    continue
                if lst_edg is None:
                    lst_edg = not edge_color
                if index == last_index:
                    loc_s_p -= 1
                go_w_ls_i(nodes, r_e[0], index, lst_edg, loc_s_p + 1, edge_color)
    if ((not edge_color or lst_edg is None) and len(nodes[index].blue_dst) != 0) or last_index == -1:
        for b_e in nodes[index].blue_dst:
            if b_e[0] == 0:
                if loc_s_p < shortest_path or shortest_path == -1:
                    shortest_path = loc_s_p + 1
                return 1
            else:
                if b_e[0] == last_index and index != last_index:
                    continue
                if index == last_index:
                    loc_s_p -= 1
                if lst_edg is None or (last_index == -1 and len(nodes[index].red_dst) != 0):
                    lst_edg = edge_color
                    edge_color = not lst_edg
                go_w_ls_i(nodes, b_e[0], index, lst_edg, loc_s_p + 1, edge_color)
    if shortest_path == 2 ** 32:
        shortest_path = -1
    return -1


class Solution:
    def shortestAlternatingPaths(self, n, red_edges, blue_edges):
        shortest_paths = []
        nodes = {}
        for i in range(0, n):
            nodes[i] = Node([], [])
            for r in red_edges:
                if r[1] == i:
                    nodes[i].red_dst.append(r)
            for b in blue_edges:
                if b[1] == i:
                    nodes[i].blue_dst.append(b)

        shortest_paths.insert(0, 0)

        for i in range(1, n):
            global shortest_path
            shortest_path = 2 ** 32
            go(nodes, i, True)
            shortest_paths.insert(i, shortest_path)

        return shortest_paths


print(Solution().shortestAlternatingPaths(
    7,
    [[0, 1], [1, 2], [3, 2], [3, 4], [4, 4]],
    [[0, 4], [0, 5], [5, 6], [4, 3], [3, 1]]
))


class TestSolution(unittest.TestCase):
    s = Solution()

    def test_case_0(self):
        result = self.s.shortestAlternatingPaths(
            n=7,
            red_edges=[[0, 1], [1, 2], [3, 2], [3, 4], [4, 4]],
            blue_edges=[[0, 4], [0, 5], [5, 6], [4, 3], [3, 1]]
        )
        self.assertEqual([0, 1, 3, 2, 1, 1, -1], result)

    def test_case_1(self):
        result = self.s.shortestAlternatingPaths(
            n=5,
            red_edges=[[0, 1], [3, 2], [1, 0], [4, 3], [2, 4]],
            blue_edges=[[2, 4], [2, 2], [1, 3]]
        )
        self.assertEqual([0, 1, 3, 2, 4], result)

    def test_case_2(self):
        result = self.s.shortestAlternatingPaths(
            n=5,
            red_edges=[[3, 2], [4, 1], [1, 4], [2, 4]],
            blue_edges=[[2, 3], [0, 4], [4, 3], [4, 4], [4, 0], [1, 0]]
        )
        self.assertEqual([0, 2, -1, -1, 1], result)

    def test_case_3(self):
        result = self.s.shortestAlternatingPaths(
            n=5,
            red_edges=[[1, 4], [0, 3]],
            blue_edges=[[3, 1], [3, 4]]
        )
        self.assertEqual([0, 2, -1, 1, 2], result)

    def test_case_4(self):
        result = self.s.shortestAlternatingPaths(
            n=5,
            red_edges=[[0, 1], [1, 2], [2, 3], [3, 4]],
            blue_edges=[[1, 2], [2, 3], [3, 1]]
        )
        self.assertEqual([0, 1, 2, 3, 7], result)

    def test_case_5(self):
        result = self.s.shortestAlternatingPaths(
            n=3,
            red_edges=[[0, 1], [1, 2]],
            blue_edges=[]
        )
        self.assertEqual([0, 1, -1], result)

    def test_case_6(self):
        result = self.s.shortestAlternatingPaths(
            n=3,
            red_edges=[[0, 1]],
            blue_edges=[[2, 1]]
        )
        self.assertEqual([0, 1, -1], result)

    def test_case_7(self):
        result = self.s.shortestAlternatingPaths(
            n=3,
            red_edges=[[1, 0]],
            blue_edges=[[2, 1]]
        )
        self.assertEqual([0, -1, -1], result)

    def test_case_8(self):
        result = self.s.shortestAlternatingPaths(n=3, red_edges=[[0, 1]], blue_edges=[[1, 2]])
        self.assertEqual([0, 1, 2], result)

    def test_case_9(self):
        result = self.s.shortestAlternatingPaths(
            n=3,
            red_edges=[[0, 1], [0, 2]],
            blue_edges=[[1, 0]]
        )
        self.assertEqual([0, 1, 1], result)

    def test_case_10(self):
        result = self.s.shortestAlternatingPaths(
            n=5,
            red_edges=[[4, 2], [3, 0], [1, 2], [2, 0], [2, 1], [3, 3], [2, 3]],
            blue_edges=[[1, 2], [1, 3], [3, 3], [2, 3], [4, 2], [2, 2], [4, 4]]
        )
        self.assertEqual([0, 1, 1], result)
