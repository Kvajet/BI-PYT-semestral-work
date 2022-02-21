import pytest

import numpy as np

import init_test
from app.src.entities.movement.Astar import Astar


class FakeLevel:
    def __init__(self, size, bool_layout):
        self.size = size
        self.bool_layout = bool_layout


@pytest.fixture
def prepare_astar_0():
    map = np.array([
        False, False, False, False,
        True, True, True, True,
        False, False, False, False
    ], dtype=bool)
    map = map.reshape((3, 4))
    level = FakeLevel((4, 3), map)
    astar = Astar(level)
    return astar


@pytest.fixture
def prepare_astar_1():
    map = np.array([
        False, False, False, False,
        True, True, False, True,
        False, False, False, False
    ], dtype=bool)
    map = map.reshape((3, 4))
    level = FakeLevel((4, 3), map)
    astar = Astar(level)
    return astar


@pytest.fixture
def prepare_astar_2():
    map = np.array([
        False,
        False,
        False,
        False,
        False,
    ], dtype=bool)
    map = map.reshape((5, 1))
    level = FakeLevel((1, 5), map)
    astar = Astar(level)
    return astar


@pytest.fixture
def prepare_astar_3():
    map = np.array([
        False,
        False,
        False,
        False,
        True,
    ], dtype=bool)
    map = map.reshape((5, 1))
    level = FakeLevel((1, 5), map)
    astar = Astar(level)
    return astar


def test_unable_to_reach(prepare_astar_0):
    astar = prepare_astar_0
    assert not astar.find_path((0, 0), (3, 2))


def test_able_to_reach(prepare_astar_1):
    astar = prepare_astar_1
    assert astar.find_path((0, 0), (3, 2)) == [
        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2)
    ]


def test_able_to_reach(prepare_astar_2):
    astar = prepare_astar_2
    assert astar.find_path((0, 0), (0, 4)) == [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4)
    ]


def test_able_to_reach(prepare_astar_3):
    astar = prepare_astar_3
    assert not astar.find_path((0, 0), (0, 4))
