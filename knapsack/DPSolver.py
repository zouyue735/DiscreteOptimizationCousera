#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import *

class DPSolver(KnapsackSolver):

    def solve(self, n: int, K: int, items: list) -> Solution:
        processed_items = self.preprocess(n, K, items)

        mat = [[0 for _n in range(0, n + 1)] for _k in range(0, K + 1)]
        for _n in range(0, n + 1):
            for _k in range(0, K + 1):
                if _n == 0:
                    mat[_k][_n] = 0
                elif _k < processed_items[_n - 1].weight:
                    mat[_k][_n] = mat[_k][_n - 1]
                else:
                    mat[_k][_n] = max(mat[_k][_n - 1], mat[_k - processed_items[_n - 1].weight][_n - 1] + processed_items[_n - 1].value)

        value = mat[K][n]
        weight = 0
        taken = [False] * n
        _k = K
        for _n in reversed(range(0, n)):
            if not mat[_k][_n + 1] == mat[_k][_n]:
                _k = _k - processed_items[_n].weight
                weight = weight + processed_items[_n].weight
                taken[_n] = True

        solution = Solution(value, weight, True, [False] * n)
        for i, item in enumerate(processed_items):
            #print(item.value, item.weight, optimum.taken[i])
            solution.taken[item.index] = taken[i]

        return solution