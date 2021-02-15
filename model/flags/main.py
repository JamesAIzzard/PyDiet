from typing import Dict

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