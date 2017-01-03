#!/usr/bin/python
# -*- coding: utf-8 -*-

from BranchAndBoundSolver import *

class LinearBound(Bound):

    def bound(self, n: int, K: int, items: list) -> float:
        value = 0
        weight = 0

        for i in items:
            if weight + i.weight <= K:
                weight = weight + i.weight
                value = value + i.value
            else:
                fraction = (K - weight) / i.weight
                weight = K
                value = value + i.value * fraction
                break

        return value