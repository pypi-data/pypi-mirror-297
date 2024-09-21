"""Dummy dataset for testing purposes."""
from typing import Any

from kedro.io import MemoryDataSet


class DummyDataset(MemoryDataSet):
    """Dummy dataset for testing purposes."""

    # pylint: disable=useless-super-delegation,too-few-public-methods
    def __init__(self, data: Any = True, copy_mode: str = None):
        super().__init__(data, copy_mode)
