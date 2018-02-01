from __future__ import absolute_import, print_function
import networkx as nx
import pyhwcomm.program as pg


class Storage:
    def __init__(self, size):
        self.size = size
    
    def size(self):
        raise NotImplementedError


class Processor:
    def __init__(self):
        pass

    def time(self, workload):
        knownTime = workload.known_run_time(self)
        if knownTime:
            return knownTime
        else:
            return 0


class CPU(Processor, Storage):
    def __init__(self, device, size):
        Storage.__init__(self, size)
        self.device = device


class GPU(Processor):
    def __init__(self, device):
        Processor.__init__(self)
        self.device = device


class NVIDIAP100(GPU):
    """An NVIDIA P100 GPU"""
    def __init__(self):
        GPU.__init__(self)


class NvidiaTitanXp(GPU):
    def __init__(self, device):
        GPU.__init__(self, device)


class GDDR5X(Storage):
    pass


class HBM2(Storage):
    pass


class Machine:
    def __init__(self):
        self.topology = nx.DiGraph()

    def execute(self, program):
        time = 0.0
        nodes = nx.topological_sort(program)
        for node in nodes:
            if isinstance(node, pg.Compute):
                pass
            elif isinstance(node, pg.Transfer):
                src = node.src
                dst = node.dst
                txSize = node.size
                link = self.topology[src][dst]['link']
                time += link.time(txSize)
            else:
                print(node)
                assert False
        return time
