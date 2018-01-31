from __future__ import print_function


class Value:
    """A value in memory"""
    def __init__(self, size):
        self.size = size


class Compute:
    def __init__(self, device=None):
        self.device = device
        self.parameters = None  # flops, reads, threads

    def __str__(self):
        return "Compute{device:" + str(self.device) + "}"


class Transfer:
    def __init__(self, size, src=None, dst=None):
        self.src = src
        self.dst = dst
        self.size = size

    def __str__(self):
        return "Transfer{src:" + str(self.src) + \
            ", dst:" + str(self.dst) + ", size:" + str(self.size) + "}"
