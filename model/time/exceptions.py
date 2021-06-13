from typing import Any

import exceptions


class BaseTimeError(exceptions.PyDietError):
    """Base error for the time module."""

    def __init__(self, subject: Any = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject


class TimeValueError(BaseTimeError):
    """Indicates the time string cannot be parsed as a valid time."""

    def __init__(self, time_value: Any, **kwargs):
        super().__init__(**kwargs)
        self.time_value = time_value


class TimeIntervalValueError(BaseTimeError):
    """Indicates the time interval cannot be interpreted in a valid way."""

    def __init__(self, time_interval: Any, **kwargs):
        super().__init__(**kwargs)
        self.time_interval = time_interval
