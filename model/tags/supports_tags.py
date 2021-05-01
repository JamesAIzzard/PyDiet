from typing import List, Optional, Dict, Any

import model
import persistence


class HasTags(persistence.HasPersistableData):
    """Class to implement tag functionality.
    Tags are the descriptive terms used to categories meals. So things like "main", "side", "drink" etc.
    """

    def __init__(self, tags: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)

        self._tags = []

        if tags is not None:
            self.load_data(data={'tags': tags})

    def has_tag(self, tag: str) -> bool:
        """Returns True/False to indicate if the instance has the specified tag."""
        return tag in self._tags

    def load_data(self, data: Dict[str, Any]) -> None:
        super().load_data(data)
        self._tags = data['tags']

    @property
    def persistable_data(self) -> Dict[str, Any]:
        data = super().persistable_data
        data['tags'] = self._tags
        return data


class HasSettableTags(HasTags):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_tag(self, tag: str) -> None:
        """Adds a tag to the instance."""
        tag = model.tags.validation.validate_tag(tag)
        if tag not in self._tags:
            self._tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Removes a tag from the instance."""
        if tag in self._tags:
            self._tags.remove(tag)
