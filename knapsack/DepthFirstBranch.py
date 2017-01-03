#!/usr/bin/python
# -*- coding: utf-8 -*-

from BranchAndBoundSolver import *

class DepthFirstBranch(Branch):

    def branch(self, n: int, K: int, items: list, tree: ItemTree) -> bool:
        while True:
            if not tree.nextItem():
                tree.walk_back()
            elif tree.has_child(True) and tree.has_child(False):
                if not tree.walk_back():
                    return False
            elif tree.has_child(True):
                tree.walk(False)
                return True
            else:
                tree.walk(True)
                return True

        return False