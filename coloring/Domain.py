#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node:

    def __init__(self, index: int, nc: int = 0, edges: list = []):
        self.index = index

        if nc:
            self.domains = set(range(0, nc))
            self.neighbours = []
            for (v1, v2) in edges:
                if v1 == index:
                    self.neighbours.append(v2)
                elif v2 == index:
                    self.neighbours.append(v1)

    def is_value(self):
        return len(domains) == 1

    def get_value(self):
        if len(domains) == 1:
            return list(domains)[0]

        return None

    def prune(self, value: int) -> bool:
        if value in domains:
            domains.remove(value)
            return True

        return False


class Domain:

    def __init__(self, nc: int = 0, ec: int = 0, edges: list = []):
        if nc:
            self.previous_state = None
            self.domain = list()

            for idx in range(0, nc):
                self.domain.append(Node(idx, nc, edges))

    def new(self):
        new_state = Domain()
        new_state.previous_state = self
        new_state.domain = list()

        for d in self.domain:
            node = Node(d.index)
            node.neighbours = d.neighbours
            node.domains = set(d.domains)
            new_state.domain.append(d)

    def is_solution(self) -> bool:
        return max(map(lambda n: len(n.domains), self.domain)) == 1