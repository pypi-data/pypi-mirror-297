from __future__ import annotations

import test_py_cpp as m


def test_add():
    assert m.add(1, 2) == 3


def test_sub():
    assert m.subtract(1, 2) == -1
