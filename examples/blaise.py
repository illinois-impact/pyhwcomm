from __future__ import print_function

import networkx as nx

from pyhwcomm import Compute, Transfer
from pyhwcomm.program import Program
from pyhwcomm.machines.blaise import Blaise
from pyhwcomm.executor import ReplayExecutor



c = Blaise()
p = Program()
p.graph.add_edge(Compute(c.cpu0, run_times={type(c.cpu0): 1e-5}), Transfer(1000, c.cpu0, c.gpu0))
e = ReplayExecutor()
elapsed = e(p, c)

print(elapsed)

