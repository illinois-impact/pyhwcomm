from __future__ import absolute_import

import networkx as nx

import pyhwcomm.program as pgm
import pyhwcomm.machine as mch

# The abstract machine
gpu0 = mch.CPU(0)
cpu0 = mch.GPU(0)

# The program components
h2d0 = pgm.Transfer(cpu0, gpu0, 25 * 50 * 4)
h2d1 = pgm.Transfer(cpu0, gpu0, 50 * 40 * 4)
kernel = pgm.Compute(gpu0)
d2h0 = pgm.Transfer(gpu0, cpu0, 25 * 40 * 4)

# Set up the program graph
SGEMM = nx.DiGraph()
SGEMM.add_edge(h2d0, kernel)
SGEMM.add_edge(h2d1, kernel)
SGEMM.add_edge(kernel, d2h0)
