"""Utility functions for the time module."""

import model


def time_is_in_interval(time: str, time_interval: str) -> bool:
    """Return True/False to indicate if the time falls inside the interval."""
    # Validate the inputs;
    time = model.time.validate_time(time)
    time_interval = model.time.validate_time_interval(time_interval)
