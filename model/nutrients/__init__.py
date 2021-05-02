import copy

from . import configs, exceptions, validation, main
from .main import (get_nutrient_primary_name,
                   PRIMARY_AND_ALIAS_NUTRIENT_NAMES,
                   GLOBAL_NUTRIENTS,
                   NUTRIENT_GROUP_NAMES,
                   OPTIONAL_NUTRIENT_NAMES,
                   get_nutrient_alias_names,
                   get_calories_per_g,
                   validate_nutrient_family_masses,
                   get_n_closest_nutrient_names)
from .nutrient import Nutrient
from .nutrient_mass import (
    NutrientMass,
    SettableNutrientMass
)
from .nutrient_ratios import (
    NutrientRatioData,
    NutrientRatio,
    SettableNutrientRatio,
    NutrientRatiosData,
    HasNutrientRatios,
    HasSettableNutrientRatios
)

# Check the configs are OK;
validation.validate_configs()

# Initialise the nutrient group names list;
main.NUTRIENT_GROUP_NAMES = configs.NUTRIENT_GROUP_DEFINITIONS.keys()

# Initialise the optional nutrients list;
main.OPTIONAL_NUTRIENT_NAMES = set(configs.ALL_PRIMARY_NUTRIENT_NAMES).difference(set(configs.MANDATORY_NUTRIENT_NAMES))

# Initialise the all known nutrients name list;
main.PRIMARY_AND_ALIAS_NUTRIENT_NAMES = copy.copy(configs.ALL_PRIMARY_NUTRIENT_NAMES)
for primary_name, aliases in configs.NUTRIENT_ALIASES.items():
    main.PRIMARY_AND_ALIAS_NUTRIENT_NAMES += aliases

# Initialise the global nutrient list;
for primary_nutrient_name in configs.ALL_PRIMARY_NUTRIENT_NAMES:
    GLOBAL_NUTRIENTS[primary_nutrient_name] = Nutrient(primary_nutrient_name)
