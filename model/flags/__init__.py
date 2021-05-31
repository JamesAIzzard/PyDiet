"""Initialisation for the flags module."""
from . import configs, validation, exceptions
from .configs import FlagImpliesNutrient
from .data_types import FlagDOFData
from .flag import Flag
from .flag_implies_nutrient import FlagImpliesNutrient
from .has_flags import HasFlags, HasSettableFlags
from .main import ALL_FLAGS, NRConflicts, get_flag, flag_has_dof, build_global_flag_list

# Check the configs are OK;
validation.validate_configs(configs)
