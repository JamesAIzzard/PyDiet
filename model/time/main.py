"""Utility functions for the time_str module."""
import time

import model


def time_is_in_interval(time_str: str, time_interval_str: str) -> bool:
    """Return True/False to indicate if the time_str falls inside the interval."""
    # Validate the inputs;
    time_str = model.time.validation.validate_time(time_str)
    time_interval_str = model.time.validation.validate_time_interval(time_interval_str)

    # Convert the strings to time objects;
    tm = time.strptime(time_str, "%H:%M")
    start_time = time.strptime(time_interval_str.split("-")[0], "%H:%M")
    end_time = time.strptime(time_interval_str.split("-")[1], "%H:%M")

    # Determine if the time is between the start and end time;
    time_in_interval = start_time <= tm <= end_time

    # If end time is the day after start time, invert the result;
    if start_time > end_time > tm:
        time_in_interval = not time_in_interval

    # Go ahead and return the result;
    return time_in_interval
