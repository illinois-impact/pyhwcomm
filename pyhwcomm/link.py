from __future__ import print_function


class Link:
    def time(self, txSize):
        return txSize / self.bandwidth(txSize) + self.latency(txSize)

    def bandwidth(self, txSize):
        raise NotImplementedError

    def latency(self, txSize):
        raise NotImplementedError

class UnknownLink(Link):
    def time(self, txSize):
        return 0.0

class AggregateLink(Link):
    def __init__(self, links):
        self.links = links

    def bandwidth(self, txSize):
        return min(l.bandwidth(txSize) for l in self.links)

    def latency(self, txSize):
        return sum(l.latency(txSize) for l in self.links)


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


class NvidiaTitanXpLink(Link):
    def bandwidth(self, txSize):
        return 547.7 * 1024 * 1024 * 1024
    def latency(self, txSize):
        return 0.0

class IBMPower8SmpBus(Link):
    def bandwidth(self, txSize):  # FIXME: made up
        return 25.0 * 1024 * 1024 * 1024
    def latency(self, txSize):
        return 0.0