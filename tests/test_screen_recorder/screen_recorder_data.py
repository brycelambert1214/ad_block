# tests/test_screen_recorder/screen_recorder_data.py

import pytest
from ad_block.screen_recorder import RecorderSettings

from data import (
    TEST_ZERO_VALUES,
    TEST_POSITIVE_INTS,
    TEST_POSITIVE_FLOATS,
    TEST_NEGATIVE_INTS,
    TEST_NEGATIVE_FLOATS,
    TEST_INVALID_TYPES,
)


# ------------------------------------------------------------
# Valid settings
# ------------------------------------------------------------

VALID_SETTINGS = [
    pytest.param(
        30,
        5,
        1,
        id="default_recording",
    ),
    pytest.param(
        60,
        5,
        1,
        id="60fps_recording",
    ),
    pytest.param(
        120,
        0.5,
        2,
        id="high_fps_short_recording",
    ),
]


# ------------------------------------------------------------
# Invalid fps
# ------------------------------------------------------------

INVALID_FPS_VALUES = [
    pytest.param(
        value,
        id=f"invalid_fps_{value}",
    )
    for value in (
        TEST_NEGATIVE_INTS
        + TEST_ZERO_VALUES[:-1]  # exclude the float zero value as it is wrong type
    )
]

INVALID_FPS_TYPES = [
    pytest.param(
        value,
        id=f"invalid_type_{name}",
    )
    for name, value in enumerate(TEST_INVALID_TYPES)
    if not isinstance(value, (int, float))
]


# ------------------------------------------------------------
# Invalid replay seconds
# ------------------------------------------------------------

INVALID_REPLAY_SECONDS_VALUES = [
    pytest.param(
        value,
        id=f"invalid_seconds_{value}",
    )
    for value in (
        TEST_NEGATIVE_FLOATS
        + TEST_NEGATIVE_INTS
        + TEST_ZERO_VALUES
    )
]

INVALID_REPLAY_SECONDS_TYPES = [
    pytest.param(
        value,
        id=f"invalid_type_{name}",
    )
    for name, value in enumerate(TEST_INVALID_TYPES)
    if not isinstance(value, (int, float))
]


# ------------------------------------------------------------
# Invalid monitors
# ------------------------------------------------------------

INVALID_MONITOR_VALUES = [
    pytest.param(
        value,
        id=f"invalid_monitor_{value}",
    )
    for value in (
        TEST_NEGATIVE_INTS
        + TEST_ZERO_VALUES[:-1]  # exclude the float zero value as it is wrong type 
    )
]

INVALID_MONITOR_TYPES = [
    pytest.param(
        value,
        id=f"invalid_type_{name}",
    )
    for name, value in enumerate(TEST_INVALID_TYPES)
    if not isinstance(value, int)
]


# ------------------------------------------------------------
# Valid replacement tests
# ------------------------------------------------------------

REPLACE_SETTINGS = [
    pytest.param(
        {"fps": 120},
        {"fps": 120},
        id="replace_fps",
    ),
    pytest.param(
        {"replay_seconds": 10},
        {"replay_seconds": 10},
        id="replace_replay_seconds",
    ),
    pytest.param(
        {"monitor": 2},
        {"monitor": 2},
        id="replace_monitor",
    ),
]

VALID_BUFFER_CAPACITIES = (
    1,
    2,
    5,
    10,
    100,
)

INVALID_BUFFER_CAPACITY_VALUES = (
    0,
    -1,
    -10,
)

INVALID_BUFFER_CAPACITY_TYPES = (
    None,
    1.5,
    "10",
    [],
    {},
    (),
    True,
)

VALID_RECORDER_SETTINGS = (
    RecorderSettings(),
    RecorderSettings(expected_fps=30),
    RecorderSettings(expected_fps=60, replay_seconds=5),
    RecorderSettings(expected_fps=90, replay_seconds=10, monitor=2),
)

INVALID_RECORDER_SETTINGS = (
    1,
    1.5,
    "settings",
    [''],  # python sees [] as None so it actually works
    {''},  # python sees {} as None so it actually works
    ('a'),  # python sees both () and ('') as None so those work
    True,
)
