import re
from typing import List


def pascal_to_snake(text: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_pascal(text: str) -> str:
    import re
    return ''.join(x.capitalize() or '_' for x in text.split('_'))


def stringify_route(route: List[str]) -> str:
    s = "."
    return s.join(route)


def listify_route(route: str) -> List[str]:
    return route.split(".")
