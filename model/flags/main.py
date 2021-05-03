from typing import Dict, List, TypedDict

import model
# Bring things in for init;
from . import configs
from .flag import Flag


class NRConflicts(TypedDict):
    """The four fields represent the following:
        - need_zero -> These nutrients ratios would need to be zero for the flag to apply.
        - need_non_zero -> These nutrient ratios would need to be non zero for the flag to apply.
        - needs_undefining -> The single nutrient ratio associated with the flag needs to be undefined.
        - preventing_undefine -> The multiple nutrient ratios that mean we can't set the flag to be undefined.
    """
    need_zero: List[str]
    need_non_zero: List[str]
    need_undefining: List[str]
    preventing_flag_undefine: List[str]


def build_global_flag_list(flag_configs: Dict) -> Dict[str, 'model.flags.Flag']:
    all_flags: Dict[str, 'model.flags.Flag'] = {}
    for flag_name, data in flag_configs.items():
        all_flags[flag_name] = Flag(flag_name=flag_name)
    return all_flags


ALL_FLAGS: Dict[str, 'model.flags.Flag'] = build_global_flag_list(configs.FLAG_CONFIGS)


def get_flag(flag_name: str) -> 'model.flags.Flag':
    """Returns a reference to the named flag from the global list."""
    # Check the name is OK first;
    flag_name = model.flags.validation.validate_flag_name(flag_name)
    return model.flags.ALL_FLAGS[flag_name]


def flag_has_dof(flag_name: str) -> bool:
    """Returns True/False to indicate if the flag has a DOF."""
    # Grab the flag first;
    flag = get_flag(flag_name)
    # Inspect and return;
    return not flag.direct_alias
