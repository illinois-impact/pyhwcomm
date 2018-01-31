from __future__ import absolute_import

import networkx as nx

import pyhwcomm.program as pgm

i0p0 = pgm.Value(100)
i1p0 = pgm.Value(100)
i0p1 = pgm.Value(100)
i1p1 = pgm.Value(100)
op0 = pgm.Value(100)
op1 = pgm.Value(100)
k0 = pgm.Compute()
k1 = pgm.Compute()
VecAddStream = nx.DiGraph()
VecAddStream.add_edge(i0p0, k0)
VecAddStream.add_edge(i1p0, k0)
VecAddStream.add_edge(k0, op0)
VecAddStream.add_edge(i0p1, k1)
VecAddStream.add_edge(i1p1, k1)
VecAddStream.add_edge(k1, op1)
