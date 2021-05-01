from typing import Any


class PyDietError(Exception):
    """Base exception for the PyDiet application."""

    def __init__(self, **kwargs):
        pass


class NameUndefinedError(PyDietError):
    def __init__(self, subject: Any = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject
