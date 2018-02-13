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

        busy_until = {}
        node_completion_times = {}

        cuda_gpus = machine.cuda_gpu()
        for k in cuda_gpus:
            gpu = cuda_gpus[k]
            busy_until[gpu] = 0.0
        for link in machine.topology.edges:
            busy_until[link] = 0.0

        for n in nx.topological_sort(program.graph):

            # print("Working on:", n)

            # get resources used by predecessors
            preds = list(program.graph.predecessors(n))
            if len(preds) == 0:
                preds_ready = 0.0
                # print("no preds")
            else:
                preds_ready = max(node_completion_times[p] for p in preds)
                # print("preds ready:", preds_ready)

            

            if isinstance(n, pgm.Compute):
                all_ready = max(preds_ready, busy_until[n.device])
                completion_time = all_ready + n.known_run_time(n.device)
                busy_until[n.device] = completion_time
                node_completion_times[n] = completion_time
            elif isinstance(n, pgm.Transfer):
                all_ready = preds_ready

                # if unknown transfer, 0 time
                if n.src == machine.unknown or n.dst == machine.unknown:
                    completion_time = all_ready
                else:
                    paths = [p for p in machine.all_paths(n.src, n.dst)]
                    path = min(machine.all_paths(n.src, n.dst), key=len)
                    edges = zip(path[:-1], path[1:])

                    for edge in edges:
                        # print(edge, "busy until", busy_until[edge])
                        all_ready = max(all_ready, busy_until[edge])
                    
                    completion_time = all_ready + machine.path_time(n.size, path)

                    for edge in edges:
                        # print("e", edge, "now busy until", completion_time)
                        busy_until[edge] = completion_time

                    if isinstance(n, pgm.Transfer):
                        print(id(n), ",", all_ready, ",", completion_time-all_ready, ",",n.src, ",",n.dst)

                node_completion_times[n] = completion_time

            else:
                print("Unexpected node:", n)
                assert False



        elapsed = max(node_completion_times.values())
        return elapsed
