from __future__ import print_function
import networkx as nx


class Storage:
    def __init__(self):
        pass


class Compute:
    def __init__(self):
        pass


class CPU(Compute, Storage):
    def __init__(self, device):
        self.device = device


class GPU(Compute, Storage):
    def __init__(self, device):
        self.device = device


class Machine:
    def __init__(self):
        self.topology = nx.DiGraph()

    def execute(self, program):
        pass
