#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import *

class Node:

    def __init__(self, item: Item, taken: bool, pruned: bool, parent, child_zero, child_one):
        self.item = item
        self.taken = taken
        self.pruned = pruned
        self.parent = parent
        self.child_zero = child_zero
        self.child_one = child_one


class ItemTree:

    def __init__(self, items: list):
        self.items = items[:]
        self.currentIdx = -1
        self.currentNode = None
        self.root_one = None
        self.root_zero = None

    def nextItem(self) -> Item:
        if self.currentIdx == len(self.items) - 1:
            return None
        else:
            return self.items[self.currentIdx + 1]

    def remainingItems(self) -> list:
        return self.items[(self.currentIdx + 1):]

    def prune(self):
        self.currentNode.pruned = True

        del self.currentNode.child_zero
        del self.currentNode.child_one

        self.currentIdx = self.currentIdx - 1
        self.currentNode = self.currentNode.parent

    def has_child(self, take: bool) -> bool:
        if self.currentIdx == len(self.items) - 1:
            return False

        if take:
            if self.currentNode:
                if self.currentNode.child_one:
                    return True
                else:
                    return False
            else:
                if self.root_one:
                    return True
                else:
                    return False
        else:
            if self.currentNode:
                if self.currentNode.child_zero:
                    return True
                else:
                    return False
            else:
                if self.root_zero:
                    return True
                else:
                    return False

    def child_pruned(self):
        child_zero = None
        child_one = None

        if self.currentNode:
            if self.currentNode.pruned:
                return True

            if not self.currentNode.child_one or not self.currentNode.child_zero:
                return False

            return self.currentNode.child_zero.pruned and self.currentNode.child_one.pruned
        else:
            if not self.root_one or not self.root_zero:
                return False

            return self.root_zero.pruned and self.root_one.pruned


    def walk(self, take: bool) -> bool:
        if self.currentIdx == len(self.items) - 1:
            return False

        if self.currentNode:
            if take:
                if not self.currentNode.child_one:
                    self.currentNode.child_one = Node(self.nextItem(), take, False, self.currentNode, None, None)

                nextNode = self.currentNode.child_one
            else:
                if not self.currentNode.child_zero:
                    self.currentNode.child_zero = Node(self.nextItem(), take, False, self.currentNode, None, None)

                nextNode = self.currentNode.child_zero
        else:
            nextNode = Node(self.nextItem(), take, False, None, None, None)
            if take:
                self.root_one = nextNode
            else:
                self.root_zero = nextNode

        if nextNode.pruned:
            return False

        self.currentIdx = self.currentIdx + 1
        self.currentNode = nextNode

        return True

    def walk_back(self) -> bool:
        if self.currentIdx == -1:
            return False

        self.currentIdx = self.currentIdx - 1
        self.currentNode = self.currentNode.parent
        return True

    def currentPath(self) -> Solution:
        if not self.currentNode:
            return None

        is_optimal = True
        taken = [self.currentNode.taken]
        value = 0
        weight = 0
        if taken[0]:
            value = self.currentNode.item.value
            weight = self.currentNode.item.weight

        node = self.currentNode.parent

        while node:
            taken.append(node.taken)

            if node.taken:
                value = value + node.item.value
                weight = weight + node.item.weight

            node = node.parent

        taken.reverse()

        return Solution(value, weight, is_optimal, taken)


class Branch:

    def branch(self, n: int, K: int, items: list, tree: ItemTree) -> bool:
        return False


class Bound:

    def bound(self, n: int, K: int, items: list) -> float:
        return sum(list(map(lambda item: item.value, items)))


class BranchAndBoundSolver(KnapsackSolver, Bound, Branch):

    def solve(self, n: int, K: int, items: list) -> Solution:
        processed_items = self.preprocess(n, K, items)
        
        tree = ItemTree(processed_items)
        optimum = super().solve(n, K, processed_items)

        while self.branch(n, K, processed_items, tree):
            currentSolution = tree.currentPath()
            #print(currentSolution)
            if currentSolution.weight > K:
                tree.prune()
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