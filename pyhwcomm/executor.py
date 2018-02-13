from __future__ import print_function

import logging

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

        gpu_busy_until = {}
        link_busy_until = {}

        print(machine.cuda_gpu())
        cuda_gpus = machine.cuda_gpu()
        for k in cuda_gpus:
            gpu = cuda_gpus[k]
            gpu_busy_until[gpu] = 0.0
        for link in machine.topology.edges:
            link_busy_until[link] = 0.0

        for n in nx.topological_sort(program.graph):
            if isinstance(n, pgm.Compute):
                logging.debug("Compute on device", n.device, "was busy until", gpu_busy_until[n.device])
                gpu_busy_until[n.device] += n.known_run_time(n.device)
            if isinstance(n, pgm.Transfer):
                print(n.src, "->", n.dst)
                paths = [p for p in machine.all_paths(n.src, n.dst)]
                path = min(machine.all_paths(n.src, n.dst), key=len)
                print(path)
                edges = zip(path[:-1], path[1:])

                busy_until = max(link_busy_until[edge] for edge in edges)
                tx_time = machine.path_time(n.size, path)

                for edge in path:
                    link_busy_until[edge] = busy_until + tx_time

            else:
                print("Unexpected node:", n)
                assert False

        gpu_elapsed = max(gpu_busy_until.values())
        link_elapsed = max(link_busy_until.values())
        return max(gpu_elapsed, link_elapsed)
