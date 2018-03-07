"""This module provide functions that transforming a pycprof profile to a pyhwcomm program""" 

from __future__ import print_function
from __future__ import absolute_import

import logging

import networkx as nx

import pycprof as cprof
from pyhwcomm.program import Program, Value, Compute
from pyhwcomm.transforms import InsertImplicitTransfers, RemoveValues
from pyhwcomm.machine import GPU

def MakeConcrete(profile, machine):
    """MakeConcrete produces a program from the profile with every node assigned to the empirical machine"""
    assert isinstance(profile, cprof.profile.Profile)

    mapping = {}

    for node in profile.graph.nodes:
        if isinstance(node, cprof.dom.Value):
            location = node.allocation.loc
            if location.type == "host":
                component = machine.cpu()[location.id_]
            elif location.type == "cuda":
                component = machine.cuda_gpu()[location.id_]
            else:
                logging.warning("Unexpected location: " + str(location))
                component = machine.unknown

            mapping[node] = Value(node.size, component)
        elif isinstance(node, cprof.dom.CudaLaunch):
            component = machine.cuda_gpu()[node.device]
            mapping[node] = Compute(component, cprof_api_id=node.id, run_times={GPU: (node.kernel_end - node.kernel_start) / 1e9})
        elif isinstance(node, cprof.dom.API):
            component = machine.cuda_gpu()[node.device]
            mapping[node] = Compute(component, cprof_api_id=node.id, run_times={GPU: (node.wall_end - node.wall_start) / 1e9})

    out = Program()
    out.graph = nx.relabel_nodes(profile.graph, mapping, copy=True)

    # Replace Values with Transfers
    out.graph = InsertImplicitTransfers()(out.graph)
    out.graph = RemoveValues()(out.graph)

    return out

def MakeAbstract(profile):
    """MakeAbstract produces a program from the profile with all locations stripped"""
    raise NotImplementedError