from __future__ import absolute_import

import networkx as nx

from ..machine import CPU, GPU, Machine
from ..link import PCIe3x16


class Blaise(Machine):
    def __init__(self):
        self.topology = nx.DiGraph()
        cpu0 = CPU(0)
        gpu0 = GPU(0)
        self.topology.add_edge(cpu0, gpu0, link=PCIe3x16())
