"""Validation functions for the time module."""
from datetime import datetime

import model


def validate_time_interval(time_interval: str) -> str:
    """Validates time interval strings of the form HH:MM-HH:MM."""

    # Split the string into two parts about the hyphen;
    start_and_end_time = time_interval.split('-')

    # Check there are two parts;
    if not len(start_and_end_time) == 2:
        raise model.time.exceptions.TimeIntervalValueError(time_interval=time_interval)

    # Format the time into double digit 24hr format;
    for n, t in enumerate(start_and_end_time):
        start_and_end_time[n] = validate_time(t)

    # Check the intervals are not the same;
    if start_and_end_time[0] == start_and_end_time[1]:
        raise model.time.exceptions.TimeIntervalValueError(time_interval=time_interval)

    # Return the interval;
    return '-'.join(start_and_end_time)


def validate_time(time: str) -> str:
    """Validates time string of the form HH:MM."""
    # Try format the time into double digit 24hr format;
    try:
        d = datetime.strptime(time, "%H:%M")
        return d.strftime("%H:%M")
    except ValueError:
        raise model.time.exceptions.TimeValueError(time_value=time)
