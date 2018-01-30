from __future__ import absolute_import

import networkx as nx

from ..machine import CPU, GPU, Machine


class Minsky(Machine):
    def __init__(self):
        self.topology = nx.DiGraph()
        cpu0 = CPU(0)
        cpu1 = CPU(1)
        gpu0 = GPU(0)
        gpu1 = GPU(1)
        gpu2 = GPU(2)
        gpu3 = GPU(3)
        self.topology.add_edge(cpu0, cpu1)
        self.topology.add_edge(cpu0, gpu0)
        self.topology.add_edge(cpu0, gpu1)
        self.topology.add_edge(gpu0, gpu1)
        self.topology.add_edge(cpu1, gpu2)
        self.topology.add_edge(cpu1, gpu3)
        self.topology.add_edge(gpu2, gpu3)
