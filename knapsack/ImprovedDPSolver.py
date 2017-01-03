#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import *

class ImprovedDPSolver(KnapsackSolver):

    def solve(self, n: int, K: int, items: list) -> Solution:
        processed_items = self.preprocess(n, K, items)

        mat = [dict() for _k in range(0, K + 1)]
        last_col = [None] * (K + 1)
        curr_col = [None] * (K + 1)
        swap = [None] * (K + 1)
        for _n in range(0, n + 1):
            print(_n)
            for _k in range(0, K + 1):
                if not _n:
                    curr_col[_k] = 0
                elif _k < processed_items[_n - 1].weight:
                    curr_col[_k] = last_col[_k]
                else:
                    curr_col[_k] = max(last_col[_k], last_col[_k - processed_items[_n - 1].weight] + processed_items[_n - 1].value)

            if _n:
                for i, (last, curr) in enumerate(zip(last_col, curr_col)):
                    # print(_n, i, last, curr)
                    if last != curr:
                        mat[i][_n - 1] = last

            swap = last_col
            last_col = curr_col
            curr_col = swap


        value = last_col[K]
        weight = 0
        taken = [False] * n
        _k = K
        for _n in reversed(range(0, n)):
            if _n in mat[_k]:
                _k = _k - processed_items[_n].weight
                weight = weight + processed_items[_n].weight
                taken[_n] = True

        solution = Solution(value, weight, True, [False] * n)
        for i, item in enumerate(processed_items):
            #print(item.value, item.weight, optimum.taken[i])
            solution.taken[item.index] = taken[i]

        return solution