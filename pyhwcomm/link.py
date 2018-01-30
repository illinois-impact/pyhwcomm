from __future__ import print_function


class Link:
    def time(self, txSize):
        return NotImplemented


class NVLink(Link):
    def time(self, txSize):
        return txSize / (80.0 * 1024 * 1024 * 1024)


class PCIe3x16(Link):
    def time(self, txSize):
        return txSize / (15.8 * 1024 * 1024 * 1024)
