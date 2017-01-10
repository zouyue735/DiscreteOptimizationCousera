#!/usr/bin/python
# -*- coding: utf-8 -*-

from Domain import *

class Solution:

    def __init__(self, colors: list):
        self.colors = colors
        self.color_count = len(set(colors))

    def is_optimal(self) -> bool:
        return False


class ColoringSolver:

    def solve(self, nc: int, ec: int, edges: list) -> Solution:
        return Solution(list(range(0, nc)))