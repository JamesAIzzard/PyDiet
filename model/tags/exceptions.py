from typing import Optional

import exceptions
import model


class BaseTagError(exceptions.PyDietError):
    """Base exception for all tag module exceptions."""

    def __init__(self, subject: Optional['model.tags.HasTags'], **kwargs):
        super().__init__(**kwargs)
        self._subject = subject


class UnknownTagError(BaseTagError):
    def __init__(self, tag: str, **kwargs):
        super().__init__(**kwargs)
        self.tag = tag
