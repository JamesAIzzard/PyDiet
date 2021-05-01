import model


def validate_tag(tag: str) -> str:
    if tag.lower() in model.tags.configs.ALL_TAGS:
        return tag
    else:
        raise model.tags.exceptions.UnknownTagError(tag=tag)
