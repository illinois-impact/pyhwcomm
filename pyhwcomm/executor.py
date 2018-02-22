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

            # print("Working on:", n, repr(n))

            # Figure out when all predecessors ready
            preds = list(program.graph.predecessors(n))
            preds_ready = None
            if len(preds) == 0:
                preds_ready = 0.0
                # print("no preds")
            else:
                # for p in preds:
                #     print("pred", p, repr(p))
                preds_ready = max(node_completion_times[p] for p in preds)
                # print("preds ready:", preds_ready)


            

            if isinstance(n, pgm.Compute):
                # Figure out when required hardware is ready
                hardware_ready = busy_until[n.device]
                # Figure out when everything is ready
                all_ready = max(preds_ready, hardware_ready)
                # Figure out when work is done
                completion_time = all_ready + n.known_run_time(n.device)
                # mark hardware as busy
                busy_until[n.device] = completion_time
            elif isinstance(n, pgm.Transfer):
                # if unknown transfer, 0 time
                if n.src == machine.unknown or n.dst == machine.unknown:
                    completion_time = preds_ready
                else:
                    paths = [p for p in machine.all_paths(n.src, n.dst)]
                    path = min(machine.all_paths(n.src, n.dst), key=len)
                    edges = zip(path[:-1], path[1:])

                    # FIXME: handle self-copy

                    hardware_ready = -1
                    for edge in edges:
                        hardware_ready = max(hardware_ready, busy_until[edge])

                    all_ready = max(hardware_ready, preds_ready)
                    # if preds_ready < hardware_ready:
                    #     print("preds were done @ ", preds_ready, "but hardware busy until", hardware_ready)
                    
                    completion_time = all_ready + machine.path_time(n.size, path)

                    for edge in edges:
                        # print("e", edge, "now busy until", completion_time)
                        busy_until[edge] = completion_time     
            else:
                print(n)
                assert False

            node_completion_times[n] = completion_time


            if isinstance(n, pgm.Transfer):
                print(id(n), ",", all_ready, ",", completion_time-all_ready, ",,,", n.src, ",", n.dst)
            elif isinstance(n, pgm.Compute):
                print(n.cprof_api_id, ",,,", all_ready, ",", completion_time-all_ready, ",", n.device, ",")

            else:
                print("Unexpected node:", n)
                assert False



        elapsed = max(node_completion_times.values())
        return elapsed
