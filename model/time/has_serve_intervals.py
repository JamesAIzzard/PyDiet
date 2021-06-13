"""Module to implement functionality associated with objects which support serve times.
For example, a recipe has a serve time_str, indicating when during the day it is typically consumed.
"""
import abc
from typing import List, Dict, Optional, Any

import model
import persistence


class HasReadableServeIntervals(persistence.YieldsPersistableData, abc.ABC):
    """Abstract base class to implement functionality to support readable serve times."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def serve_intervals_data(self) -> List[str]:
        """Returns the serve times data for the instance."""
        raise NotImplementedError

    def can_be_served_at(self, time: str) -> bool:
        """Returns True/False to indicate if the instance can be served at the specified time_str."""
        # Cycle through all the intervals, and immediately return True if we
        # have an interval on the instance that matches the time_str.
        for serve_interval in self.serve_intervals_data:
            if model.time.time_is_in_interval(
                    time_str=time,
                    time_interval_str=serve_interval
            ):
                return True

        # Ahh, OK, we didn't find anything, so no, we can't serve this instance at the
        # proposed time_str.
        return False

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for the instance."""
        data = super().persistable_data

        data["serve_intervals"] = self.serve_intervals_data

        return data


class HasSettableServeIntervals(HasReadableServeIntervals, persistence.CanLoadData):
    """Class to implement functionality associated with settable serve times."""

    def __init__(self, serve_times_data: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)

        # Create a list of serve times locally;
        self._serve_times_data = []

        if serve_times_data is not None:
            self.load_data({"serve_intervals": serve_times_data})

    @property
    def serve_intervals_data(self) -> List[str]:
        """Returns serve times data for the instance."""
        return self._serve_times_data

    def add_serve_interval(self, serve_interval: str):
        """Adds a serve interval to the instance."""
        self._serve_times_data.append(serve_interval)

    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads instance data."""
        super().load_data(data)

        if "serve_intervals" not in data.keys():
            return

        self._serve_times_data = data['serve_intervals']
