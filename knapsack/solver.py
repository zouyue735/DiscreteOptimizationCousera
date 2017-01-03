#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import *
from BranchAndBoundSolver import * 
from MyBranchAndBoundSolvers import *
from DPSolver import *
from ImprovedDPSolver import *
from HybridSolver import *

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    
    # prepare the solution in the specified output format

    # solver = base.KnapsackSolver()
    # solver = BranchAndBoundSolver()
    # solver = MyBranchAndBoundSolver()
    if item_count < 300:
        solver = ImprovedDPSolver()
    elif item_count < 500:
        solver = MyBranchAndBoundSolver()
    elif item_count < 2000:
        solver = ImprovedDPSolver()
    else:
        solver = ImprovedDPSolver()
    # solver = ImprovedDPSolver()
    # solver = HybridSolver()

    solution = solver.solve(item_count, capacity, items)

    output_data = str(solution.value) + ' ' + str(solution.is_optimal * 1) + '\n'
    output_data += ' '.join(map(lambda taken: str(taken * 1), solution.taken))
    #print('\n'.join(map(lambda item: str(item.value) + ',' + str(item.weight), items)))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

