from __future__ import absolute_import, print_function
import networkx as nx
import pyhwcomm.program as pg

class Component:
    pass

class Storage(Component):
    def __init__(self, size):
        self.size = size

class Processor(Component):
    def __init__(self):
        pass

    def time(self, workload):
        knownTime = workload.known_run_time(self)
        if knownTime:
            return knownTime
        else:
            return 0.0


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
    def __init__(self, device):
        GPU.__init__(self, device)


class NvidiaTitanXp(GPU):
    def __init__(self, device):
        GPU.__init__(self, device)


class GDDR5X(Storage):
    pass


class HBM2(Storage):
    pass


class MachineView:
    def __getitem__(self, key):
        raise NotImplementedError

class CPUView(MachineView):
    def __init__(self):
        self.dict = {}
    def __getitem__(self, key):
        return self.dict[key]

class Machine:
    def __init__(self):
        self.topology = nx.DiGraph()

    def cuda_gpu(self):
        devices = {}
        for node in self.topology:
            if isinstance(node, GPU):
                devices[node.device] = node
        return devices

    def cpu(self):
        cpus = {}
        for node in self.topology:
            if isinstance(node, CPU):
                cpus[node.device] = node
        return cpus

    def all_paths(self, src, dst):
        return nx.all_simple_paths(self.topology, src, dst)

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
