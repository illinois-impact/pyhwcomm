from __future__ import print_function


class Compute:
    def __init__(self, device):
        self.device = device


class Transfer:
    def __init__(self, src, dst, size):
        self.src = src
        self.dst = dst
        self.size = size
