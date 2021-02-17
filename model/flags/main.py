from typing import Dict, List

from model import flags

all_flags: Dict[str, 'flags.Flag'] = {}


def init_global_flags():
    """Build the global flags dictionary"""
    for flag_name, data in flags.configs.flag_data.items():
        all_flags[flag_name] = flags.Flag(
            name=flag_name,
            nutrient_relations=data["nutrient_relations"],
            direct_alias=data["direct_alias"]
        )


def all_flag_names() -> List[str]:
    """Return a list of all flag names."""
    return list(all_flags.keys())
