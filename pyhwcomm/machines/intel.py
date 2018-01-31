from __future__ import absolute_import
from pyhwcomm.machine import CPU, GPU, Machine
from pyhwcomm.link import QPI48, PCIe3x16


class Intel(Machine):
    def __init__(self):
        Machine.__init__(self)
        self.cpu0 = CPU(0)
        self.cpu1 = CPU(1)
        self.topology.add_edge(self.cpu0, self.cpu1, link=QPI48())
        self.gpu0 = GPU(0)
        self.topology.add_edge(self.cpu1, self.gpu0, link=PCIe3x16())
