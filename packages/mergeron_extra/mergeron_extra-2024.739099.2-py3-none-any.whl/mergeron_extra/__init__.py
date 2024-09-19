from __future__ import annotations

from pathlib import Path

import numpy as np

_PKG_NAME: str = Path(__file__).parent.stem

VERSION = "2024.739097.4"

__version__ = VERSION

DATA_DIR: Path = Path.home() / _PKG_NAME
"""
Defines a subdirectory named for this package in the user's home path.

If the subdirectory doesn't exist, it is created on package invocation.
"""
if not DATA_DIR.is_dir():
    DATA_DIR.mkdir(parents=False)


np.set_printoptions(precision=18)
