#!/usr/bin/python
# -*- coding: utf-8 -*-

from ColoringSolver import *

class NotEqualConstraint(Constraint):

    def __init__(self, v_idx1: int, v_idx2: int):
        self.v_idx1 = v_idx1
        self.v_idx2 = v_idx2

    # TODO

    def feasible(self, domain: Domain) -> bool:
        if len(domain.domain[v_idx1].domains) == 1 and len(domain.domain[v_idx2].domains) == 1:
            return list(domain.domain[v_idx1].domains)[0] != list(domain.domain[v_idx2].domains)[0]
        else:
            return True

    def prune(self, domain: Domain):
        if len(domain.domain[v_idx1].domains) == 1:
            domain.domain[v_idx2].domains.remove()
        elif len(domain.domain[v_idx2].domains) == 1:
            domain.domain[v_idx1].domains.remove(list(domain.domain[v_idx2].domains)[0])
