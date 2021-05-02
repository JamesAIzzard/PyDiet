from . import configs, validation, exceptions
from .flag import Flag
from .has_flags import HasFlags, HasSettableFlags, FlagDOFData
from .main import ALL_FLAGS, ALL_FLAG_NAMES, FLAGS_WITH_DOF, FLAGS_WITHOUT_DOF, FlagImpliesNutrient, NRConflicts

# Initialise the derived globals;
for flag_name, data in configs.FLAG_DATA.items():

    # Initialise the flag instance;
    ALL_FLAGS[flag_name] = Flag(flag_name=flag_name)

    # Add the name to the list of all flag names;
    ALL_FLAG_NAMES.append(flag_name)

    # If it has DOF;
    if data['direct_alias'] is True:
        FLAGS_WITHOUT_DOF.append(flag_name)
    else:
        FLAGS_WITH_DOF.append(flag_name)
