"""Flag functionality"""
from typing import Dict, List

import model
from . import configs, exceptions


class Flag:
    """Models a global food flag.
    Notes:
        This class defines the relationships between a particular flag and its nutrients.
        The instance specific data associated with any given flag is stored on the
        instances of HasFlags and HasSettableFlags, and should not be confused with this
        global definition of the flag.
    """

    def __init__(self, flag_name: str):
        # Validate the flag name;
        # We can't use the normal validator function here, becuase it will check the global
        # flag list, and this constructor will be called to populate the global flag list.
        if flag_name not in configs.FLAG_CONFIGS.keys():
            raise exceptions.FlagNameError(flag_name=flag_name)

        self._name = flag_name
        self._nutrient_relations: Dict[str, 'model.flags.FlagImpliesNutrient'] = \
            configs.FLAG_CONFIGS[flag_name]["nutrient_relations"]
        self._direct_alias: bool = configs.FLAG_CONFIGS[flag_name]["direct_alias"]

    @property
    def name(self) -> str:
        """Returns the flag's name."""
        return self._name

    @property
    def direct_alias(self) -> bool:
        """Returns True/False to indicate if the flag is a direct alias."""
        return self._direct_alias

    @property
    def related_nutrient_names(self) -> List[str]:
        """Returns a list of names of related nutrients."""
        return list(self._nutrient_relations.keys())

    def get_implication_for_nutrient(self, nutrient_name: str) -> 'model.flags.FlagImpliesNutrient':
        """Returns the implication associated with the named nutrient."""
        # Check we are using the primary nutrient name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)
        # Return the relations for this name;
        try:
            return self._nutrient_relations[nutrient_name]
        except KeyError:
            raise model.flags.exceptions.NutrientNotRelatedError(
                flag_name=self.name,
                nutrient_name=nutrient_name
            )

    def nutrient_ratio_matches_relation(self, nutrient_ratio: 'model.nutrients.ReadonlyNutrientRatio') -> bool:
        """Returns True/False/None to indicate if the nutrient relation
        matches the nutrient ratio supplied."""
        # Grab the implication first;
        implication = self.get_implication_for_nutrient(nutrient_ratio.nutrient_mass.nutrient.primary_name)

        # If implication is zero;
        if implication is model.flags.FlagImpliesNutrient.zero:
            return not nutrient_ratio.subject_g_per_host_g > 0

        # If implication is non-zero;
        elif implication is model.flags.FlagImpliesNutrient.non_zero:
            return nutrient_ratio.subject_g_per_host_g > 0
