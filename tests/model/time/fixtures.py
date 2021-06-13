"""Test fixtures for the time module."""
from typing import List

import model


class HasReadableServeIntervalsTestable(model.time.HasReadableServeIntervals):
    """Minimal implementation of HasReadbaleServeIntervals to allow testing."""

    def __init__(self, serve_intervals_data: List[str], **kwargs):
        super().__init__(**kwargs)

        self._serve_intervals_data = serve_intervals_data

    @property
    def serve_intervals_data(self) -> List[str]:
        """Returns serve intervals data for the class."""
        return self._serve_intervals_data
