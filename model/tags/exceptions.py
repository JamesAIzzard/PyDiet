"""Defines exceptions for the tags module."""
from typing import Optional

import exceptions
import model


class BaseTagError(exceptions.PyDietError):
    """Base exception for all tag module exceptions."""

    def __init__(self, subject: Optional['model.tags.HasReadableTags']=None, **kwargs):
        super().__init__(**kwargs)
        self._subject = subject


class UnknownTagError(BaseTagError):
    """Indicating the tag that bas been used is not recognised by the system."""
    def __init__(self, tag: str, **kwargs):
        super().__init__(**kwargs)
        self.tag = tag
