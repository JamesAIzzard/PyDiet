from typing import List, Dict

ALL_PRIMARY_NUTRIENT_NAMES: List[str] = [
    "foo",
    "foobing",
    "bar",
    "gihumve",
    "fejaolka",
    "foobar",
    "docbe",
    "cufmagif",
    "bazing",
    "tirbur",
    "fillydon",
    "busskie",
    "regatur",
    "bingtong"
]

MANDATORY_NUTRIENT_NAMES: List[str] = [
    "regatur",
    "bingtong",
    "cufmagif",
]

NUTRIENT_ALIASES: Dict[str, List[str]] = {
    "docbe": ["anatino", "vibdo", "sefling"],
    "cufmagif": ["impstern", "golbuot", "terrnig"],
}

NUTRIENT_GROUP_DEFINITIONS: Dict[str, List[str]] = {
    "regatur": ["tirbur", "cufmagif"],
    "docbe": ["regatur", "bar"],
    "busskie": ["bingtong", "tirbur"],
    "fillydon": ["bazing", "foo", "fejaolka"]
}

CALORIE_NUTRIENTS: Dict[str, float] = {
    "fillydon": 1,
    "busskie": 2,
    "regatur": 3,
    "bingtong": 4
}