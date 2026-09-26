# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.types.test_iec_array
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

import copy

import pytest

from srci.types.iec import IecArray


def test_st_indices() -> None:
    a = IecArray(1, [10, 20, 30])
    assert (a.lower, a.upper, len(a)) == (1, 3, 3)
    assert a[1] == 10 and a[3] == 30
    a[2] = 99
    assert list(a) == [10, 99, 30]


@pytest.mark.parametrize("index", [0, 4, -1])
def test_out_of_range(index: int) -> None:
    a = IecArray(1, [1, 2, 3])
    with pytest.raises(IndexError):
        _ = a[index]
    with pytest.raises(IndexError):
        a[index] = 0


def test_fixed_length() -> None:
    a = IecArray(1, [1, 2])
    with pytest.raises(TypeError):
        a.append(1)
    with pytest.raises(TypeError):
        a.pop()
    with pytest.raises(TypeError):
        a.clear()
    with pytest.raises(TypeError):
        a.insert(0, 1)
    with pytest.raises(ValueError):
        a[0:1] = [1, 2, 3]
    a[0:2] = [5, 6]  # slices work on the underlying 0 based list
    assert list(a) == [5, 6]


def test_copy_keeps_bounds() -> None:
    a = IecArray(5, [[1], [2]])
    b = copy.deepcopy(a)
    c = copy.copy(a)
    assert isinstance(b, IecArray) and b.lower == 5 and b == a
    b[5].append(9)
    assert a[5] == [1]
    assert isinstance(c, IecArray) and c.lower == 5
