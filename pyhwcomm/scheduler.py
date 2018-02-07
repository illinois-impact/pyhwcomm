"""
schedulers take an abstract program and a machine
and produce a concrete program
"""

from __future__ import print_function

import networkx as nx
import pyhwcomm.program as pgm
import pyhwcomm.transforms as pt
# import pyhwcomm.machine as mchn

import pycprof.dom


class Scheduler:
    def __init__(self):
        pass

class TrivialScheduler(Scheduler):
    """TrivialScheduler assigns everything to device 0"""
    def __init__(self):
        Scheduler.__init__(self)

    def __call__(self, program, machine):
        p = pt.AssignSinks()(program, machine.cpu0)
        p = pt.AssignSources()(p, machine.cpu0)
        p = pt.AssignKernels()(p, machine.gpu0)
        p = pt.AssignValuesBySuccessor()(p)
        p = pt.InsertTransfers()(p)
        p = pt.RemoveValues()(p)
        concrete = p
        return concrete

class GreedyScheduler(Scheduler):
    """GreedyScheduler assigns everything to the earliest available hardware"""
    def __init__(self):
        Scheduler.__init__(self)

    def __call__(self, program, machine):

        out = program.copy()

        computes = {}
        engines = {}
        links = {}
        for i, gpu in machine.cuda_gpu():
            computes[gpu] = 0.0
            engines[gpu] = 0.0

        for n in nx.topological_sort(program):
            if isinstance(n, program.Compute):
                for i, gpu in machine.cuda_gpu():
                    # figure out how long it would take to get the input data to each gpu
                    for input_value in program.predecessors(n):

                        

                        assert isinstance(input_value, pycprof.dom.Value)



                        paths = machine.all_paths(src, dst)
                        for path in paths:
                            path.



                first_compute = min(computes, key=computes.get)
                computes[first_compute] += first_compute.time(n)



