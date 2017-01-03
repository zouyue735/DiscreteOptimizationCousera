#!/usr/bin/python
# -*- coding: utf-8 -*-

from DepthFirstBranch import *
from LinearBound import *

class MyBranchAndBoundSolver(BranchAndBoundSolver, LinearBound, DepthFirstBranch):
	pass