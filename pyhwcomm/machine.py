from __future__ import absolute_import, print_function
import networkx as nx
import pyhwcomm.program as pg
from pyhwcomm.link import AggregateLink, UnknownLink

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

class Unknown(Processor, Storage):
    def __init__(self):
        Storage.__init__(self, Ellipsis)

class CPU(Processor, Storage):
    def __init__(self, device, size):
        Storage.__init__(self, size)
        self.device = device
    
    def __str__(self):
        return "CPU-" + str(self.device)


class GPU(Processor):
    def __init__(self, device):
        Processor.__init__(self)
        self.device = device


class NVIDIAP100(GPU):
    """An NVIDIA P100 GPU"""
    def __init__(self, device):
        GPU.__init__(self, device)

    def __str__(self):
        return "NVIDIA-P100-" + str(self.device)


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
        self.unknown = Unknown()
        self.topology = nx.DiGraph()
        self.topology.add_node(self.unknown)

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

    def add_node(self, n, **attr):
        self.topology.add_node(n, attr)

    def add_edge(self, src, dst, link):
        self.topology.add_edge(src, dst, link=link)

    def all_paths(self, src, dst):
        paths = list(nx.all_simple_paths(self.topology, src, dst))
        return paths

    def path_time(self, size, path):
        links = [self.topology[src][dst]['link'] for src,dst in zip(path[:-1], path[1:])]
        agg = AggregateLink(links)
        return agg.latency(size) + size / agg.bandwidth(size)

def component_type_from_str(s):
    return {
        "NvidiaP100": NVIDIAP100
    }[s]