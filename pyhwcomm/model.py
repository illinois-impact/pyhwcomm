from __future__ import print_function


class Device:
    def __init__(self, device):
        self.device = device


class CPU(Device):
    def __init__(self, device):
        self.device = device


class GPU(Device):
    pass


class Data:
    def __init__(self, size, device, pageable):
        self.device = device
        self.pageable = pageable
        self.size = size


class Machine:
    def __init__(self):
        return

    def estimate_time(self, src, dst):
        return
