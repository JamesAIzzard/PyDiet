"""Validation functions for the tags module."""
from typing import List

import model


def validate_tag(tag: str) -> str:
    """Validates a single tag."""
    if tag.lower() in model.tags.configs.ALL_TAGS:
        return tag
    else:
        raise model.tags.exceptions.UnknownTagError(tag=tag)


def validate_tags(tags: List[str]) -> List[str]:
    """Validates a list of tags."""
    for tag in tags:
        _ = validate_tag(tag)
    return tags
