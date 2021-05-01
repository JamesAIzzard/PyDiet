import enum
from typing import Dict, List, TypedDict

import model

ALL_FLAGS: Dict[str, 'model.flags.Flag'] = {}
ALL_FLAG_NAMES: List[str] = []
FLAGS_WITH_DOF: List[str] = []
FLAGS_WITHOUT_DOF: List[str] = []


class FlagImpliesNutrient(enum.Enum):
    zero = 1
    non_zero = 2


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
