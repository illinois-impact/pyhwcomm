from __future__ import print_function

import networkx as nx

class Value:
    """A value in memory"""
    def __init__(self, size, device):
        self.size = size
        self.device = device


class Compute:
    def __init__(self, device=None, cprof_api_id=None, run_times={}):
        self.device = device
        self.known_run_times = run_times
        self.parameters = None  # flops, reads, threads

    def __str__(self):
        return "Compute{device:" + str(self.device) + "}"

    def known_run_time(self, processor_ty):
        """returns a known time for a computation to run on a particular processor"""
        return self.known_run_times[processor_ty]

    def resources(self):
        return [self.device]


# A compute node that has parameters we know
class ParamterizedComputeMixin(object):
    def __init__(self, f32_ops):
        self.f32_ops = f32_ops

class ParameterizedTransfer(object):
    def __init__(self, bytes):
        self.bytes = bytes

# A program node that occupies one or more devices
class BoundMixin(object):
    def __init__(self, devices):
        self.devices = devices

# A program node for which we have empirical data
class EmpiricalMixin(object):
    def __init__(self):
        self.observed_times = {}
    def observed(self, component_ty, time):
        self.observed_times[component_ty] = time



class Transfer:
    def __init__(self, size, src=None, dst=None):
        self.src = src
        self.dst = dst
        self.size = size

    def __str__(self):
        return "Transfer{src:" + str(self.src) + \
            ", dst:" + str(self.dst) + ", size:" + str(self.size) + "}"

    def resources(self):
        return [self.src, self.dst]

class Program:
    def __init__(self):
        self.graph = nx.DiGraph()