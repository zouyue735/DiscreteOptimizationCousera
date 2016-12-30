#!/usr/bin/python
# -*- coding: utf-8 -*-

import base

class BranchAndBoundSolver(KnapsackSolver):

    def estimate(self, n: int, K: int, items: list) -> int:
        return list(sum(list(map(lambda item: item.value, items))))

    def solve(self, n: int, K: int, items: list) -> Solution:
        tree = ItemTree()



Node = namedtuple("Node", ['item', 'taken', 'pruned', 'parent', 'child_zero', 'child_one'])

class ItemTree:

    items = []
    currentIdx = -1
    currentNode = None

    def __init__(self, items: list):
        self.items = items[:]

    def nextItem(self) -> Item:
        if self.currentIdx == len(self.items) - 1:
            return None
        else:
            return self.items[self.currentIdx + 1]

    def remainingItems(self) -> list:
        return self.items[(self.currentIdx + 1):]

    def walk(self, take: bool) -> bool:
        if currentIdx == len(items) - 1:
            return False

        if currentNode:
            if take:
                if not currentNode.child_one:
                    currentNode.child_one = Node(nextItem(), take, False, currentNode, None, None)

                nextNode = currentNode.child_one
            else:
                if not currentNode.child_zero:
                    currentNode.child_zero = Node(nextItem(), take, False, currentNode, None, None)

                nextNode = currentNode.child_zero
        else:
            nextNode = Node(nextItem(), take, False, None, None, None)

        if nextNode.pruned:
            return False

        currentIdx++
        currentNode = nextNode
        return True

    def currentPath(self) -> Solution:
        if not currentNode:
            return None

        is_optimal = True
        taken = [currentNode.taken]
        value = 0
        if taken:
            value = currentNode.item.value

        node = currentNode

        while node.parent:
            taken.append(node.taken)

            if node.taken:
                value = value + node.item.value

            node = node.parent

        return Solution(value, is_optimal, taken.reverse())