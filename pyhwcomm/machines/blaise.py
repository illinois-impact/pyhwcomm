from __future__ import absolute_import

import networkx as nx

from ..machine import CPU, Machine, GDDR5X, NvidiaTitanXp
from ..link import PCIe3x16, NvidiaTitanXpLink


class Blaise(Machine):
    """Blaise is a model for the theoretical performance of blaise"""
    def __init__(self):
        self.topology = nx.DiGraph()
        self.cpu0 = CPU(0, 24 * 1024 * 1024 * 1024)
        self.gpu0 = NvidiaTitanXp(0)
        self.gpu0mem = GDDR5X(12 * 1024 * 1024 * 1024)

        # CPU/GPU links
        self.topology.add_edge(self.cpu0, self.gpu0, link=PCIe3x16())
        self.topology.add_edge(self.gpu0, self.cpu0, link=PCIe3x16())

        # GPU internal links
        self.topology.add_edge(self.gpu0, self.gpu0mem, link=NvidiaTitanXpLink())
        self.topology.add_edge(self.gpu0mem, self.gpu0, link=NvidiaTitanXpLink())


class BlaiseEmpirical(Machine):
    """BlaiseEmpirical is a model for the empirical performance of blaise"""
    def __init__(self):
        raise NotImplementedError