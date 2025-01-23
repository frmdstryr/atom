# --------------------------------------------------------------------------------------
# Copyright (c) 2025, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# --------------------------------------------------------------------------------------
from datetime import datetime

import pytest

from atom.api import Atom, Value

pytest.importorskip("pytest_benchmark")


@pytest.mark.benchmark(group="getattr-default")
def test_getattr_default_access_speed(benchmark):
    class Test(Atom):
        x = Value()
    benchmark.pedantic(lambda: Test().x, rounds=100000, warmup_rounds=10, iterations=100)


@pytest.mark.benchmark(group="getattr-access")
def test_getattr_access_speed(benchmark):
    class Test(Atom):
        x = Value()
    t = Test()
    t.x # Do default
    benchmark.pedantic(lambda: t.x, rounds=100000, warmup_rounds=10, iterations=100)


@pytest.mark.benchmark(group="setattr")
def test_setattr_speed(benchmark):
    class Test(Atom):
        x = Value()
    counter = 0
    t = Test(x=counter)

    def setter():
        nonlocal counter
        counter += 1
        t.x = counter
    benchmark.pedantic(setter, rounds=100000, warmup_rounds=10, iterations=100)
