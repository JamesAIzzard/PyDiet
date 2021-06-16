"""Fixtures for testing the tags module."""
from typing import List

import model

class HasReadableTagsTestable(model.tags.HasReadableTags):
    """Minimal implementation to allow testing of the HasReadableTags class."""

    def __init__(self, tags: List[str], **kwargs):
        super().__init__(**kwargs)

        self._tags = tags

    @property
    def tags(self) -> List[str]:
        """Return the tags for the instance."""
        return self._tags
