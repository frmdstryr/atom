# --------------------------------------------------------------------------------------
# Copyright (c) 2022, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# --------------------------------------------------------------------------------------
import copyreg
from datetime import datetime

import pytest

from atom.api import Atom, Bool, Int, Float, List, Range, Str, Typed, observe

try:
    import pytest_benchmark
    BENCHMARK_INSTALLED = True
except ImportError as e:
    BENCHMARK_INSTALLED = False


class AtomBase(Atom):
    def __getstate_py__(self):
        state = {}
        state.update(getattr(self, "__dict__", {}))
        slots = copyreg._slotnames(type(self))
        if slots:
            for name in slots:
                state[name] = getattr(self, name)
        for key in self.members():
            state[key] = getattr(self, key)
        return state

    def __setstate_py__(self, state):
        for key, value in state.items():
            setattr(self, key, value)


def test_getstate_member_slots_error():
    class Test(Atom):
        __slots__ = ("a", "b")

    Test.__slotnames__ = None
    v = Test()
    with pytest.raises(SystemError):
        v.__getstate__()


def test_getstate_member_error():
    class Test(Atom):
        created = Typed(datetime, factory=float)

    v = Test()
    with pytest.raises(TypeError):
        v.__getstate__()


def test_getstate():
    class Test(Atom):
        x = Int(3)
        y = Int(2)
    t = Test()
    t.__getstate__() == {"x": 3, "y": 2}


@pytest.mark.skipif(not BENCHMARK_INSTALLED, reason="benchmark is not installed")
@pytest.mark.benchmark(group="getstate")
@pytest.mark.parametrize("fn", ("c", "py"))
def test_bench_getstate(benchmark, fn):
    class Test(AtomBase):
        first_name = Str("First")
        last_name = Str("Last")
        age = Range(low=0)
        debug = Bool(False)
        items = List(default=[1, 2, 3])

    expected = {
        "first_name": "First",
        "last_name": "Last",
        "age": 0,
        "debug": False,
        "items": [1, 2, 3],
    }
    p = Test()
    if fn == "py":
        func = p.__getstate_py__
    else:
        func = p.__getstate__

    def task():
        assert func() == expected

    benchmark(task)


@pytest.mark.skipif(not BENCHMARK_INSTALLED, reason="benchmark is not installed")
@pytest.mark.benchmark(group="getstate-dict")
@pytest.mark.parametrize("fn", ("c", "py"))
def test_bench_getstate_dict(benchmark, fn):
    class Foo:
        def __init__(self):
            self.count = 1

    class Test(AtomBase, Foo):
        title = Str("Title")
        enabled = Bool(True)
        category = Str("Main")
        tags = List(default=["foo", "bar"])

    expected = {
        "count": 1,
        "title": "Title",
        "enabled": True,
        "category": "Main",
        "tags": ["foo", "bar"],
    }

    p = Test()
    p.count = 1
    if fn == "py":
        func = p.__getstate_py__
    else:
        func = p.__getstate__

    def task():
        assert func() == expected

    benchmark(task)


@pytest.mark.skipif(not BENCHMARK_INSTALLED, reason="benchmark is not installed")
@pytest.mark.benchmark(group="getstate-slots")
@pytest.mark.parametrize("fn", ("c", "py"))
def test_bench_getstate_slots(benchmark, fn):
    class Test(AtomBase):
        __slots__ = ("foo", "bar")
        name = Str("Name")
        enabled = Bool(True)
        rating = Float()
        created = Typed(datetime)
        tags = List(default=["foo", "bar"])

    now = datetime.now()
    expected = {
        "foo": 1,
        "bar": True,
        "name": "Name",
        "enabled": True,
        "rating": 0.0,
        "created": now,
        "tags": ["foo", "bar"],
    }

    p = Test()
    p.foo = 1
    p.bar = True
    p.created = now
    if fn == "py":
        func = p.__getstate_py__
    else:
        func = p.__getstate__

    def task():
        assert func() == expected

    benchmark(task)


@pytest.mark.skipif(not BENCHMARK_INSTALLED, reason="benchmark is not installed")
@pytest.mark.benchmark(group="state")
@pytest.mark.parametrize("fn", ("c", "py"))
def test_bench_setstate(benchmark, fn):
    class Test(AtomBase):
        x = Int()
        y = Int()

    if fn == "py":
        def task():
            t = Test()
            t.__setstate_py__({"x": 1, "y": 2})
            assert t.x == 1
            assert t.y == 2
    else:
        def task():
            t = Test()
            t.__setstate__({"x": 1, "y": 2})
            assert t.x == 1
            assert t.y == 2

    benchmark(task)


def test_setstate():
    class Test(Atom):
        x = Int()
        y = Int()
    t = Test()
    t.__setstate__({"x": 1, "y": 2})
    assert t.x == 1
    assert t.y == 2


def test_setstate_errors(caplog):
    class Test(AtomBase):
        x = Int()
        y = Int()
    t = Test()
    with pytest.raises(TypeError):
        t.__setstate__() # Incorrect number of args
    with pytest.raises(TypeError):
        t.__setstate__({}, False) # Incorrect number of args
    with pytest.raises(AttributeError):
        t.__setstate__(None)  # Not a mapping (no items() method)
    with pytest.raises(AttributeError):
        t.__setstate__(["z"]) # Not a mapping (has no items() method)
    with pytest.raises(AttributeError):
        t.__setstate__({"z": 3}) # Invalid attribute
