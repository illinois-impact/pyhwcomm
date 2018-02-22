from __future__ import print_function

import networkx as nx

class Value:
    """A value in memory"""
    def __init__(self, size, device):
        self.size = size
        self.device = device


class Compute:
    def __init__(self, device=None, cprof_api_id=None, run_times={}):
        self.device = device
        self.known_run_times = run_times
        self.parameters = None  # flops, reads, threads
        self.cprof_api_id = cprof_api_id

    def __str__(self):
        return "Compute{device:" + str(self.device) + "}"

    def known_run_time(self, processor):
        """returns a known time for a computation to run on a particular processor"""
        for known_proc in self.known_run_times:
            time = self.known_run_times[known_proc]
            # print(processor, known_proc, type(processor))
            if processor == known_proc:
                return time
            elif isinstance(processor, known_proc):
                return time
        return None

    def resources(self):
        return [self.device]



class Transfer:
    def __init__(self, size, src=None, dst=None):
        self.src = src
        self.dst = dst
        self.size = size

    def __str__(self):
        return "Transfer{src:" + str(self.src) + \
            ", dst:" + str(self.dst) + ", size:" + str(self.size) + "}"

    def resources(self):
        return [self.src, self.dst]

class Program:
    def __init__(self):
        self.graph = nx.DiGraph()