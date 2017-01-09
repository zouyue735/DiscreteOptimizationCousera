#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import *
from MyBranchAndBoundSolvers import *
from ImprovedDPSolver import *
from random import *

class PruneNode(Node):

    def __init__(self, item: Item, taken: bool, pruned: bool, parent, child_zero, child_one, n: int, K: int):
        Node.__init__(self, item, taken, pruned, parent, child_zero, child_one)
        self.n = n - 1
        self.K = K
        if taken:
            self.K = K - item.weight

        self.complexity = (self.n + 1) * (self.K + 1)


class PruneTree(ItemTree):

    def __init__(self, n: int, K: int, items: list):
        ItemTree.__init__(self, items)
        self.complexity = self._complexity(n, K)
        self.n = n
        self.K = K

    def walk_back(self) -> bool:
        if self.currentIdx == -1:
            return False

        self.currentIdx = self.currentIdx - 1
        self.currentNode = self.currentNode.parent
        return True

    def prune(self):
        # print(self.currentIdx)

        self.currentNode.pruned = True

        self._update_complexity_path(self.currentNode)

        del self.currentNode.child_zero
        del self.currentNode.child_one

        self.currentIdx = self.currentIdx - 1
        self.currentNode = self.currentNode.parent

    def walk(self, take: bool) -> bool:
        if self.currentIdx == len(self.items) - 1:
            return False

        new_node = False

        if self.currentNode:
            if take:
                if not self.currentNode.child_one:
                    self.currentNode.child_one = PruneNode(self.nextItem(), take, False, self.currentNode, None, None, self.currentNode.n, self.currentNode.K)
                    new_node = True

                nextNode = self.currentNode.child_one
            else:
                if not self.currentNode.child_zero:
                    self.currentNode.child_zero = PruneNode(self.nextItem(), take, False, self.currentNode, None, None, self.currentNode.n, self.currentNode.K)
                    new_node = True

                nextNode = self.currentNode.child_zero
        else:
            if take:
                if not self.root_one:
                    self.root_one = PruneNode(self.nextItem(), take, False, None, None, None, self.n, self.K)
                    new_node = True

                nextNode = self.root_one
            else:
                if not self.root_zero:
                    self.root_zero = PruneNode(self.nextItem(), take, False, None, None, None, self.n, self.K)
                    new_node = True

                nextNode = self.root_zero

        if nextNode.pruned:
            return False

        self.currentIdx = self.currentIdx + 1
        self.currentNode = nextNode

        if new_node:
            self._update_complexity_path(self.currentNode)

        return True

    def _update_complexity_path(self, node: Node):
        current = node

        while current:
            if current.n == 0:
                current.complexity = 0
            else:
                current.complexity = min(current.complexity, self._node_complexity(current.child_zero, current.n - 1, current.K) + self._node_complexity(current.child_one, current.n - 1, current.K - self.items[self.n - current.n].weight))
            # print(current.complexity, _n)
            current = current.parent

        self.complexity = min(self.complexity, self._node_complexity(self.root_zero, self.n - 1, self.K) + self._node_complexity(self.root_one, self.n - 1, self.K - self.items[0].weight))

    def _node_complexity(self, node: Node, n: int, K: int) -> int:
        if K <= 0:
            return 0

        if not node:
            return self._complexity(n, K)

        if node.K <= 0:
            return 0

        if node.pruned:
            return 0

        return node.complexity

    def _complexity(self, n: int, K: int) -> int:
        return (K + 1) * (n + 1)



class HybridSolver(KnapsackSolver, LinearBound, DepthFirstBranch):

    def __init__(self):
        self.previous_complexity = 0
        self.complexity = 0
        self.iteration = 0

    def preprocess(self, n: int, K: int, items: list) -> list:
        # return sorted(items, key = lambda x: x.value / x.weight, reverse = True)
        return sorted(items, key = lambda x: (x.weight), reverse = True)

    def bound(self, n: int, K: int, items: list) -> float:
        sorted_items = super().preprocess(n, K, items)

        value = 0
        weight = 0

        for i in sorted_items:
            if weight + i.weight <= K:
                weight = weight + i.weight
                value = value + i.value
            else:
                fraction = (K - weight) / i.weight
                weight = K
                value = value + i.value * fraction
                break

        return value        

    def branch(self, n: int, K: int, items: list, tree: PruneTree) -> bool:
        # print(tree.currentIdx)
        # print('-----1---------')

        while tree.walk_back():
            # print('-----2---------')
            if not tree.has_child(True):
                tree.walk(True)
                return True

            if not tree.has_child(False):
                tree.walk(False)
                return True

        while tree.has_child(True) and tree.has_child(False):
            tree.walk(choice([True, False]))
            while tree.child_pruned() and tree.currentIdx >= 0:
                tree.prune()

        # print('-----4---------')

        if not tree.has_child(True):
            if not tree.walk(True):
                return False
        elif not tree.has_child(False):
            if not tree.walk(False):
                return False

        self.iteration = self.iteration + 1
        self.complexity = tree.complexity

        if self.previous_complexity > self.complexity:
            print(self.iteration, self.previous_complexity - self.complexity)
            self.iteration = 0

        self.previous_complexity = self.complexity
        return True

    def solve(self, n: int, K: int, items: list) -> Solution:
        processed_items = super().preprocess(n, K, items)
        optimum = super().solve(n, K, processed_items)

        processed_items = self.preprocess(n, K, items)
        tree = PruneTree(n, K, processed_items)

        print(tree.complexity)

        while self.branch(n, K, processed_items, tree):
            currentSolution = tree.currentPath()
            if currentSolution.weight > K:
                tree.prune()
                continue

            estimation = self.bound(n, K - currentSolution.weight, tree.remainingItems()) + currentSolution.value
            if estimation <= optimum.value:
                tree.prune()
            elif not tree.nextItem():
                if currentSolution.value > optimum.value:
                    optimum = currentSolution

            if not tree.complexity:
                print(tree.root_one.pruned, tree.root_zero.pruned, optimum.value)

        solution = Solution(optimum.value, optimum.weight, optimum.is_optimal, [False] * n)
        for i, item in enumerate(processed_items):
            #print(item.value, item.weight, optimum.taken[i])
            solution.taken[item.index] = optimum.taken[i]
                    
        return solution