"""This module provide functions that transforming a pycprof profile to a pyhwcomm program""" 

import networkx as nx

import pycprof.profile as cprof
from pyhwcomm.program import Program, Value

def MakeConcrete(profile, machine):
    """MakeConcrete produces a program from the profile with every node assigned to the empirial machine"""
    assert isinstance(profile, pycprof.profile.Profile)

    out = Program()
    out.graph = profile.graph.copy()

    for node in out.nodes:
        if isinstance(node, cprof.Value):
            if node.allocation.
            component = machine.cuda_gpu

            node = Value(value.size, value.device)
        programValue = Value(value.size, value.device)
        out.graph.add_node(programValue)
        pass

    raise NotImplementedError
    return nx.DiGraph()

def MakeAbstract(profile):
    """MakeAbstract produces a program from the profile with all locations stripped"""
    raise NotImplementedError