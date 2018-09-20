from __future__ import absolute_import

import networkx as nx

import pyhwcomm.program as pgm

# input 0 part 0
i0p0 = pgm.Value(100) # input 0 part 0
i1p0 = pgm.Value(100) # input 0 part 1
i0p1 = pgm.Value(100)
i1p1 = pgm.Value(100)
op0 = pgm.Value(100) # output part 0
op1 = pgm.Value(100)
k0 = pgm.Compute()
k1 = pgm.Compute()

VecAddStream = nx.DiGraph()

# part 0 of two inputs to produce output part 0
VecAddStream.add_edge(i0p0, k0)
VecAddStream.add_edge(i1p0, k0)
VecAddStream.add_edge(k0, op0)

# output part 1
VecAddStream.add_edge(i0p1, k1)
VecAddStream.add_edge(i1p1, k1)
VecAddStream.add_edge(k1, op1)
