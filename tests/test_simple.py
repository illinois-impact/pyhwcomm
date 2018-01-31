# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

from __future__ import print_function

import networkx as nx

from pyhwcomm import Compute, Transfer
from pyhwcomm.machines.blaise import Blaise
from pyhwcomm.scheduler import TrivialScheduler
import pyhwcomm.program as pgm


def test_success():
    assert True


def test_scheduler():
    c = Blaise()

    i0p0 = pgm.Value(100)
    i1p0 = pgm.Value(100)
    i0p1 = pgm.Value(100)
    i1p1 = pgm.Value(100)
    op0 = pgm.Value(100)
    op1 = pgm.Value(100)
    k0 = pgm.Compute()
    k1 = pgm.Compute()
    vecAddStream = nx.DiGraph()
    vecAddStream.add_edge(i0p0, k0)
    vecAddStream.add_edge(i1p0, k0)
    vecAddStream.add_edge(k0, op0)
    vecAddStream.add_edge(i0p1, k1)
    vecAddStream.add_edge(i1p1, k1)
    vecAddStream.add_edge(k1, op1)

    s = TrivialScheduler()
    p = s(vecAddStream, c)

    c.execute(p)

    assert True


def test_blaise():
    c = Blaise()
    p = nx.DiGraph()
    p.add_edge(Compute(c.cpu0), Transfer(1000, c.cpu0, c.gpu0))
    elapsed = c.execute(p)
    print(elapsed)
    assert True
