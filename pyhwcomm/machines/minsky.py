from __future__ import absolute_import
from ..machine import CPU, GPU, Machine


class Minsky(Machine):
    def __init__(self):
        Machine.__init__(self)
        self.cpu0 = CPU(0)
        self.cpu1 = CPU(1)
        self.gpu0 = GPU(0)
        self.gpu1 = GPU(1)
        self.gpu2 = GPU(2)
        self.gpu3 = GPU(3)
        self.topology.add_edge(self.cpu0, self.cpu1)
        self.topology.add_edge(self.cpu0, self.gpu0)
        self.topology.add_edge(self.cpu0, self.gpu1)
        self.topology.add_edge(self.gpu0, self.gpu1)
        self.topology.add_edge(self.cpu1, self.gpu2)
        self.topology.add_edge(self.cpu1, self.gpu3)
        self.topology.add_edge(self.gpu2, self.gpu3)
