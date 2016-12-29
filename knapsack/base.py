#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])
Solution = namedtuple("Solution", ['value', 'is_optimal', 'taken'])

class KnapsackSolver:

    def solve(self, n: int, K: int, items: list) -> Solution:
        # a trivial greedy algorithm for filling the knapsack
        # it takes items in-order until the knapsack is full
        value = 0
        weight = 0
        taken = [0]*len(items)

        for item in items:
            if weight + item.weight <= K:
                taken[item.index] = 1
                value += item.value
                weight += item.weight

        return Solution(value, 0, taken)