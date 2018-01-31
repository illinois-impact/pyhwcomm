from __future__ import print_function


class Link:
    def time(self, txSize):
        return txSize / self.bandwidth(txSize) + self.latency(txSize)

    def bandwidth(self, txSize):
        raise NotImplementedError

    def latency(self, txSize):
        raise NotImplementedError


class NVLink(Link):
    def bandwidth(self, txSize):
        return 80.0 * 1024 * 1024 * 1024

    def latency(self, txSize):
        return 0.0


class PCIe3x16(Link):
    def bandwidth(self, txSize):
        return 15.8 * 1024 * 1024 * 1024

    def latency(self, txSize):
        return 0.0


class QPI48(Link):
    """4.8GHz QPI Link"""
    def bandwidth(self, txSize):
        return 4.8 * 1024 * 1024 * 1024 * 2 * 16 / 8

    def latency(self, txSize):
        return 0.0
