#!/usr/bin/python
# -*- coding: utf-8 -*-

from ColoringSolver import *

class Constraint:

    def feasible(self, domain: Domain) -> bool:
        return True

    def prune(self, domain: Domain) -> bool:
        return False


class ConstraintStore:

    def __init__(self, constraints: list):
        self.previous_state = None
        self.constraints = constraints

    def new(self):
        new_state = ConstraintStore(list(self.constraints))
        new_state.previous_state = self

    def add(self, constraint: Constraint):
        self.constraints.append(constraint)

    def feasible(self, domain: Domain) -> bool:
        for constraint in reversed(self.constraints):
            if not constraint.feasible(domain):
                return False

        return True

    def prune(self, domain: Domain):
        pruned = False
        for constraint in reversed(self.constraints):
            pruned = constraint.prune(domain) or pruned

        while pruned:
            for constraint in reversed(self.constraints):
                pruned = constraint.prune(domain) or pruned


class Search:

    def search(self, domain: Domain) -> Constraint:
        return None


class NotEqualConstraint(Constraint):

    def __init__(self, v_idx1: int, v_idx2: int):
        self.v_idx1 = v_idx1
        self.v_idx2 = v_idx2

    def feasible(self, domain: Domain) -> bool:
        if domain[v_idx1].is_value() and domain[v_idx2].is_value():
            return domain[v_idx1].get_value() != domain[v_idx2].get_value()
        else:
            return True

    def prune(self, domain: Domain) -> bool:
        if domain[v_idx1].is_value():
            return domain.domain[v_idx2].prune(domain[v_idx1].get_value())
        elif domain[v_idx2].is_value():
            return domain.domain[v_idx1].prune(domain[v_idx2].get_value())

        return False


class CPColoringSolver(ColoringSolver):

    def solve(self, nc: int, ec: int, edges: list) -> Solution:
        domain = Domain(nc, ec, edges)
        constraint_store = ConstraintStore([NotEqualConstraint(v1, v2) for (v1, v2) in edges])

        solution = super().solve(nc, ec, edges)
        # TODO
        while domain.

        return Solution(list(range(0, nc)))

