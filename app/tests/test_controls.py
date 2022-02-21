import pytest

import init_test
from app.src.controls.Controls import Controls


@pytest.fixture
def prepare_controls():
    controls = Controls(None)
    return controls


def test_increment(prepare_controls):
    control = prepare_controls
    control.increment()
    assert control._pressed_keys_cnt == 1


def test_decrement(prepare_controls):
    control = prepare_controls
    control.decrement()
    assert control._pressed_keys_cnt == -1


def test_active_controls(prepare_controls):
    control = prepare_controls
    assert not control.active_controls()
    control.increment()
    assert control.active_controls()
    control.decrement()
    control.decrement()
    assert not control.active_controls()
