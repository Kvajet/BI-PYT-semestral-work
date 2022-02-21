import pytest

import init_test
from app.src.entities.Hitbox import Hitbox


config = dict(
    tile_size=16
)


@pytest.fixture
def prepare_hit_box_0():
    hb = Hitbox((41, 4), (32, 32), (2, 0))
    return hb


@pytest.fixture
def prepare_hit_box_1():
    hb = Hitbox((12, 184), (10, 10), (2, 0))
    return hb


@pytest.fixture
def prepare_hit_box_2():
    hb = Hitbox((12, 184), (10, 10), (2, 0), 50)
    return hb


@pytest.mark.parametrize(
    'pos_x, pos_y, size_x, size_y, res_x, res_y',
    [
        (41, 4, 32, 32, 16, 16),
        (41, 4, 12, 184, 6, 92),
        (41, 4, 0, 0, 0, 0),
        (41, 4, 16, 16, 8, 8)
    ]
)
def test_half_size(pos_x, pos_y, size_x, size_y, res_x, res_y):
    hb = Hitbox((pos_x, pos_y), (size_x, size_y), [False])
    assert hb.half_size() == (res_x, res_y)


@pytest.mark.parametrize(
    'pos_x, pos_y, size_x, size_y, res_x, res_y',
    [
        (41, 4, 32, 32, 2, 0),
        (16, 32, 12, 184, 1, 2),
        (17, 0, 0, 0, 1, 0),
        (32, 16, 16, 16, 2, 1)
    ]
)
def test_at_pos(pos_x, pos_y, size_x, size_y, res_x, res_y):
    hb = Hitbox((pos_x, pos_y), (size_x, size_y), [False])
    assert hb.at_pos() == (res_x, res_y)


def test_hit_miss(prepare_hit_box_0, prepare_hit_box_1):
    assert prepare_hit_box_0.hit(prepare_hit_box_0)
    assert not prepare_hit_box_0.hit(prepare_hit_box_1)
    assert not prepare_hit_box_1.hit(prepare_hit_box_0)


# works after scale
def test_hit_scaled(prepare_hit_box_0, prepare_hit_box_2):
    assert prepare_hit_box_0.hit(prepare_hit_box_0)
    assert prepare_hit_box_0.hit(prepare_hit_box_2)
    assert prepare_hit_box_2.hit(prepare_hit_box_0)
