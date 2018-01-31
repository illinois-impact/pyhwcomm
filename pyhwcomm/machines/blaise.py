from __future__ import absolute_import

import networkx as nx

from ..machine import CPU, GPU, Machine
from ..link import PCIe3x16


class Blaise(Machine):
    def __init__(self):
        self.topology = nx.DiGraph()
        self.cpu0 = CPU(0)
        self.gpu0 = GPU(0)
        self.topology.add_edge(self.cpu0, self.gpu0, link=PCIe3x16())
        self.topology.add_edge(self.gpu0, self.cpu0, link=PCIe3x16())
