from __future__ import print_function

import networkx as nx
import pyhwcomm.program as pgm
import pyhwcomm.transforms as pt
# import pyhwcomm.machine as mchn


class Executor:
    def __init__(self):
        pass


class ReplayExecutor(Executor):
    """ReplayExecutor runs a program on a machine"""

    def __init__(self):
        Executor.__init__(self)

    def __call__(self, program, machine):

        gpu_available = {}
        link_available = {}

        for gpu in machine.cuda_gpu:
            gpu_available[gpu.device] = 0.0
        for path in machine.paths:
            for edge in path:
                link_available[edge] = 0.0

        for n in nx.dag_topological_sort(program.graph):
            if isinstance(n, pgm.Compute):
                gpu_available[n.device] += n.known_run_time
            if isinstance(n, pgm.Transfer):

                path = machine.path(n.src, n.dst)
                busy_until = max(link_available[edge] for edge in path)

                tx_time = machine.tx_time(n.size, path)

                for edge in path:
                    link_available[edge] = busy_until + tx_time

            else:
                print("Unexpected node:", n)
                assert False

        gpu_elapsed = max(gpu_available.values())
        link_elapsed = max(link_available.values())
        return max(gpu_elapsed, link_elapsed)
