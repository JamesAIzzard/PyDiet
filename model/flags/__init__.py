from . import configs, validation, exceptions, main
from .flag import Flag
from .has_flags import HasFlags, HasSettableFlags, FlagDOFData
from .main import ALL_FLAGS, FlagImpliesNutrient, NRConflicts, get_flag, flag_has_dof, build_global_flag_list

# Init the global flags list;
main.ALL_FLAGS = main.build_global_flag_list(configs.FLAG_CONFIGS)
