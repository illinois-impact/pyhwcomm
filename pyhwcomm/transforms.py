from __future__ import absolute_import
from __future__ import print_function

import pyhwcomm.program as pgm
import pyhwcomm.machine as mchn

class Transform:
    """Transform a graph"""
    pass

class OverrideSinks(Transform):
    """Assign sinks to device"""
    def __call__(self, g, dev):
        out = g.copy()
        for node, outDegree in g.out_degree():
            if outDegree == 0:
                node.device = dev
        return out


class OverrideSources(Transform):
    """Assign sources to device"""
    def __call__(self, g, dev):
        out = g.copy()
        for node, inDegree in g.in_degree():
            if inDegree == 0:
                node.device = dev
        return out


class AssignValuesBySuccessor(Transform):
    def __call__(self, g):
        out = g.copy()
        for node in out:
            if isinstance(node, pgm.Value):
                if not node.device:
                    if out.out_degree(node) > 0:
                        node.device = list(g.successors(node))[0].device
        return out


class AssignKernels(Transform):
    """Assign kernels to device"""
    def __call__(self, g, device):
        out = g.copy()
        for node in out:
            if isinstance(node, pgm.Compute):
                node.device = device
        return out


class InsertTransfers(Transform):
    def __call__(self, g):
        out = g.copy()
        newTxs = []
        for node in out:
            for pred in out.predecessors(node):
                if pred.device != node.device:
                    if isinstance(pred, pgm.Value):
                        newTxs += [(pred, node, pgm.Transfer(
                            pred.size, pred.device, node.device))]
                    elif isinstance(node, pgm.Value):
                        newTxs += [(pred, node, pgm.Transfer(
                            node.size, pred.device, node.device))]
                    else:
                        assert False
        for tup in newTxs:
            pred, node, tx = tup
            out.add_edge(pred, tx)
            out.add_edge(tx, node)
        return out


class RemoveValues(Transform):
    """ Remove all Values from a program, and connect predecessors to successors"""
    def __call__(self, g):
        out = g.copy()
        toRemove = []
        for node in out:
            if isinstance(node, pgm.Value):
                toRemove += [node]

        for node in toRemove:
            preds = out.predecessors(node)
            succs = out.successors(node)
            for p in preds:
                for s in succs:
                    out.add_edge(p, s)
            out.remove_node(node)

        return out