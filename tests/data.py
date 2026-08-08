"""
General reusable test data.

This file contains deterministic test inputs that can be reused across
multiple test suites. Package-specific pytest parameterization should be
created in the corresponding test package directories.
"""

import random
import numpy as np


# ------------------------------------------------------------
# Deterministic random generators
# ------------------------------------------------------------

_RANDOM_SEED = 8675309

_rng = random.Random(_RANDOM_SEED)
_np_rng = np.random.default_rng(_RANDOM_SEED)


# ------------------------------------------------------------
# Numeric test data
# ------------------------------------------------------------

TEST_ZERO_VALUES = [
    0,
    0.0,
]


TEST_POSITIVE_INTS = [
    _rng.randint(1, 1_000_000)
    for _ in range(100)
]


TEST_POSITIVE_FLOATS = [
    _rng.uniform(0.001, 1000.0)
    for _ in range(100)
]


TEST_NEGATIVE_INTS = [
    -_rng.randint(1, 1_000_000)
    for _ in range(100)
]


TEST_NEGATIVE_FLOATS = [
    -_rng.uniform(0.001, 1000.0)
    for _ in range(100)
]


# ------------------------------------------------------------
# Common small sizes
# ------------------------------------------------------------

TEST_SMALL_POSITIVE_INTS = [
    1,
    2,
    5,
    10,
    100,
]


# ------------------------------------------------------------
# Invalid Python types
# ------------------------------------------------------------

TEST_INVALID_TYPES = [
    None,

    # Strings
    "",
    "string",

    # Boolean
    True,
    False,

    # Lists
    [],
    [1, 2, 3],

    # Tuples
    (),
    (1, 2, 3),

    # Sets
    set(),
    {1, 2, 3},

    # Dictionaries
    {},
    {"key": "value"},

    # Bytes
    b"",
    b"bytes",

    # Complex
    1 + 2j,

    # Object
    object(),

    # Callable
    lambda x: x,

    # NumPy array
    np.array([1, 2, 3]),
]


# ------------------------------------------------------------
# Image/frame data
# ------------------------------------------------------------

TEST_FRAME_SMALL = np.zeros(
    (10, 10, 3),
    dtype=np.uint8,
)


TEST_FRAME_BLACK = np.zeros(
    (1080, 1920, 3),
    dtype=np.uint8,
)


TEST_FRAME_WHITE = np.full(
    (10, 10, 3),
    255,
    dtype=np.uint8,
)


TEST_FRAME_GRAY = np.full(
    (10, 10, 3),
    127,
    dtype=np.uint8,
)


TEST_FRAME_RANDOM = _np_rng.integers(
    0,
    256,
    size=(10, 10, 3),
    dtype=np.uint8,
)


# ------------------------------------------------------------
# String/text data
# ------------------------------------------------------------

TEST_STRINGS = [
    "",
    "test",
    "hello world",
    "quantum computing",
    "screen recorder",
]


TEST_LONG_STRING = """In the realm where circuits hum and glow,
A tapestry of digits weaves, intricate flow.
Data streams like rivers, winding and deep,
Through valleys of knowledge where secrets we keep.

Once barren lands of thoughts unexplored,
Now fields of connection, unity restored.
With every byte, a tale unspools,
Crafting our futures, forging new tools.

The currents of information, swift as a breeze,
"Bring forth the answers, unravel life's keys.
From mountains of storage to oceans of cloud,
The whispers of wisdom, both soft and loud.

In the heart of the network, where visions entwine,
We dance with the algorithms, intricate design.
Each pulse of a server, a heartbeat divine,
Creating a symphony, an endless line.

Yet heed the warnings, as rivers can flood,
With torrents of chaos, a muddied sea of mud.
For every creation bears shadows of plight,
In the hands of the wielders lies the balance of light.

So let us navigate these currents with care,
Empowered by knowledge, with courage to dare.
For though technology flows like rivers untamed,
In our choices, the future is ultimately framed"""


# ------------------------------------------------------------
# Miscellaneous objects
# ------------------------------------------------------------

TEST_NONE = None

TEST_OBJECT = object()