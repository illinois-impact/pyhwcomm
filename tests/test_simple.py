# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import networkx as nx

from pyhwcomm import Compute, Transfer


def test_success():
    assert True


def test_simple():

    p = nx.DiGraph()
    p.add_edge(Compute(), Transfer(0, 0, 0))

    assert True
