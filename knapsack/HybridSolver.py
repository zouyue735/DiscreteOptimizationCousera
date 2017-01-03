#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import *
from MyBranchAndBoundSolvers import *
from ImprovedDPSolver import *

class PruneNode:

    def __init__(self, item: Item, taken: bool, pruned: bool, parent, child_zero, child_one, complexity):
        super.__init__(self, item, taken, pruned, parent, child_zero, child_one)
        self.complexity = complexity


class PruneTree(ItemTree):

    def walk(self, take: bool) -> bool:
        if self.currentIdx == len(self.items) - 1:
            return False

        if self.currentNode:
            if take:
                if not self.currentNode.child_one:
                    self.currentNode.child_one = PruneNode(self.nextItem(), take, False, self.currentNode, None, None)

                nextNode = self.currentNode.child_one
            else:
                if not self.currentNode.child_zero:
                    self.currentNode.child_zero = PruneNode(self.nextItem(), take, False, self.currentNode, None, None)

                nextNode = self.currentNode.child_zero
        else:
            nextNode = PruneNode(self.nextItem(), take, False, None, None, None, self.complexity())
            if take:
                self.root_one = nextNode
            else:
                self.root_zero = nextNode

        if nextNode.pruned:
            return False

        self.currentIdx = self.currentIdx + 1
        self.currentNode = nextNode

        return True

    def sub_tree_complexity(self, n: int, K: int) -> int:
        return min(self.complexity(n, K), self.node_complexity(n - 1, K - self.items[0].weight, self.root_one) + self.node_complexity(n - 1, K, self.root_zero))

    def node_complexity(self, n: int, K: int, node: Node) -> int:
        if not node:
            return self.complexity(n, K)

        if node.pruned:
            return 0

        if K < node.item.weight:
            return 0

        return min(self.complexity(n, K), self.node_complexity(n - 1, K - node.item.weight, node.child_one) + self.node_complexity(n - 1, K, node.child_zero))

    def complexity(self, n: int, K: int) -> int:
        return (K + 1) * (n + 1)



class HybridSolver(KnapsackSolver, LinearBound, DepthFirstBranch):


    def __init__(self):
        self.previous_complexity = 0
        self.complexity = 0
        self.iteration = 0

    def preprocess(self, n: int, K: int, items: list) -> list:
        return sorted(items, key = lambda x: x.value / x.weight, reverse = True)

    def branch(self, n: int, K: int, items: list, tree: PruneTree) -> bool:
        b = super().branch(n, K, items, tree)

        self.iteration = self.iteration + 1
        self.complexity = tree.sub_tree_complexity(n, K)

        if self.previous_complexity > self.complexity:
            print(self.iteration, self.previous_complexity - self.complexity)
            self.iteration = 0

        self.previous_complexity = self.complexity
        return b        

    def solve(self, n: int, K: int, items: list) -> Solution:
        processed_items = self.preprocess(n, K, items)

        tree = PruneTree(processed_items)
        optimum = super().solve(n, K, processed_items)

        print(tree.sub_tree_complexity(n, K))

        while self.branch(n, K, processed_items, tree):
            currentSolution = tree.currentPath()
            if currentSolution.weight > K:
                tree.prune()
                # print(tree.currentIdx)
                continue

            estimation = self.bound(n, K - currentSolution.weight, tree.remainingItems()) + currentSolution.value
            if estimation <= optimum.value:
                tree.prune()
            elif not tree.nextItem():
                if currentSolution.value > optimum.value:
                    optimum = currentSolution

        solution = Solution(optimum.value, optimum.weight, optimum.is_optimal, [False] * n)
        for i, item in enumerate(processed_items):
            #print(item.value, item.weight, optimum.taken[i])
            solution.taken[item.index] = optimum.taken[i]
                    
        return solution