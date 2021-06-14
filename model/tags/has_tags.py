"""Defines functionality associated with tagging types of meal components."""
import abc
from typing import List, Dict, Optional, Any

import model
import persistence


class HasReadableTags(persistence.YieldsPersistableData, abc.ABC):
    """Implements functionality associated with objects which have readable tags."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def tags(self) -> List[str]:
        """Returns a list of all tags associated with the instance."""
        raise NotImplementedError

    def has_tag(self, tag: str) -> bool:
        """Returns True/False to indicate if the instance has the specified tag."""
        # Validate the tag first;
        tag = model.tags.validation.validate_tag(tag)
        # All OK, check if tag is present & return.
        return tag in self.tags

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns persistable data for the instance."""
        data = super().persistable_data
        data['tags'] = self.tags
        return data


class HasSettableTags(HasReadableTags, persistence.CanLoadData):
    """Implements functionality associated with objects which ahve settable tags."""

    def __init__(self, tag_data: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)

        self._tags = []

        if tag_data is not None:
            self.load_data({"tags": tag_data})

    @property
    def tags(self) -> List[str]:
        """Returns a list of tags associated with the instance."""
        return self._tags

    def add_tags(self, tags: List[str]) -> None:
        """Adds a tag to the instance."""
        tags = model.tags.validation.validate_tags(tags)
        for tag in tags:
            if tag not in self._tags:
                self._tags.append(tag)

    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads data onto the instance."""
        super().load_data(data)

        # If we got some data;
        if "tags" in data.keys():
            # Validate it;
            tags = model.tags.validation.validate_tags(data['tags'])

            # Place it on the instance;
            self._tags = tags
