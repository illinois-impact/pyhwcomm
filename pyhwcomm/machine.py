from __future__ import absolute_import, print_function
import networkx as nx
import .program as pg


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
        time = 0.0
        nodes = nx.topological_sort(program)
        for node in nodes:
            if type(node) == pg.Compute:
                pass
            elif type(node) == pg.Transfer:
                src = node.src
                dst = node.dst
                txSize = node.size
                path = self.topology[src][dst]
                time += path.time(txSize)
            else:
                print(node)
                assert False
        return time
