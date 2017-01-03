#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])
Solution = namedtuple("Solution", ['value', 'weight', 'is_optimal', 'taken'])

class KnapsackSolver:

    def preprocess(self, n: int, K: int, items: list) -> list:
        return sorted(items, key = lambda x: x.value / x.weight, reverse = True)

    def solve(self, n: int, K: int, items: list) -> Solution:
        # a trivial greedy algorithm for filling the knapsack
        # it takes items in-order until the knapsack is full
        processed_items = self.preprocess(n, K, items)

        value = 0
        weight = 0
        taken = [0]*len(processed_items)

        for item in processed_items:
            if weight + item.weight <= K:
                taken[item.index] = 1
                value += item.value
                weight += item.weight

        solution = Solution(value, weight, False, taken)

        return solution