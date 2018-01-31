# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

from __future__ import print_function

import networkx as nx

from pyhwcomm import Compute, Transfer
from pyhwcomm.machines.blaise import Blaise
from pyhwcomm.scheduler import TrivialScheduler
from pyhwcomm.programs.vecaddstream import VecAddStream


def test_success():
    assert True


def test_scheduler():
    c = Blaise()
    s = TrivialScheduler()
    p = s(VecAddStream, c)
    c.execute(p)

    assert True


def test_blaise():
    c = Blaise()
    p = nx.DiGraph()
    p.add_edge(Compute(c.cpu0), Transfer(1000, c.cpu0, c.gpu0))
    elapsed = c.execute(p)
    print(elapsed)
    assert True
