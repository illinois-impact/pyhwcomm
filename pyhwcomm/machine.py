from __future__ import absolute_import, print_function
import networkx as nx
import pyhwcomm.program as pg


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
            if isinstance(node, pg.Compute):
                pass
            elif isinstance(node, pg.Transfer):
                src = node.src
                dst = node.dst
                txSize = node.size
                link = self.topology[src][dst]['link']
                print(link)
                time += link.time(txSize)
            else:
                print(node)
                assert False
        return time
