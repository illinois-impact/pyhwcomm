from __future__ import absolute_import
from pyhwcomm.machine import CPU, NVIDIAP100, Machine
from pyhwcomm.link import IBMPower8SmpBus, NVLink


class Minsky(Machine):
    def __init__(self):
        Machine.__init__(self)
        self.cpu0 = CPU(0, 256 * 1024 * 1024 * 1024)
        self.cpu1 = CPU(1, 256 * 1024 * 1024 * 1024)
        self.add_edge(self.cpu0, self.cpu1, IBMPower8SmpBus())
        self.add_edge(self.cpu1, self.cpu0, IBMPower8SmpBus())
        self.gpu0 = NVIDIAP100(0)
        self.gpu1 = NVIDIAP100(1)
        self.gpu2 = NVIDIAP100(2)
        self.gpu3 = NVIDIAP100(3)
        self.add_edge(self.cpu0, self.gpu1, NVLink())
        self.add_edge(self.cpu0, self.gpu0, NVLink())
        self.add_edge(self.cpu1, self.gpu2, NVLink())
        self.add_edge(self.cpu1, self.gpu3, NVLink())
        self.add_edge(self.gpu0, self.cpu0, NVLink())
        self.add_edge(self.gpu0, self.gpu1, NVLink())
        self.add_edge(self.gpu1, self.cpu0, NVLink())
        self.add_edge(self.gpu1, self.gpu0, NVLink())
        self.add_edge(self.gpu2, self.cpu1, NVLink())
        self.add_edge(self.gpu2, self.gpu3, NVLink())
        self.add_edge(self.gpu3, self.cpu1, NVLink())
        self.add_edge(self.gpu3, self.gpu2, NVLink())

