from typing import Dict, List, Optional

from model import nutrients, flags


class Flag:
    """Models a global food flag.
    Notes:
        This class defines the relationships between a particular flag and its nutrients.
        The instance specific data associated with any given flag is stored on the
        instances of HasFlags and HasSettableFlags, and should not be confused with this
        global definition of the flag.
    """

    def __init__(self, name: str,
                 nutrient_relations: Optional[Dict[str, flags.FlagImpliesNutrient]] = None,
                 direct_alias: bool = False):
        """
        Args:
            name: The flag name.
            nutrient_relations (Dict[str, 'FlagImpliesNutrient']): Dictionary of related nutrient names,
                and what the True flag would imply about the mass of the named nutrient in the subject.
            direct_alias (bool): Indicates if the flag is completely defined by its nutrient relations.
        """

        # Dissallow direct alias if there are no nutrient relations;
        if direct_alias and len(nutrient_relations) == 0:
            raise ValueError("A flag cannot be a direct alias without nutrient relations.")

        self._name = name
        self._nutrient_relations = {}
        self._direct_alias = direct_alias

        # Populate the nutrient relations info if provided;
        if nutrient_relations is not None:
            for nutrient_name, implication in nutrient_relations.items():
                nutrient_name = nutrients.get_nutrient_primary_name(nutrient_name)
                self._nutrient_relations[nutrient_name] = implication

    @property
    def name(self) -> str:
        return self._name

    @property
    def direct_alias(self) -> bool:
        return self._direct_alias

    @property
    def related_nutrient_names(self) -> List[str]:
        """Returns a list of names of related nutrients."""
        return list(self._nutrient_relations.keys())

    def get_implication_for_nutrient(self, nutrient_name: str) -> flags.FlagImpliesNutrient:
        """Returns the implication associated with the named nutrient."""
        nutrient_name = nutrients.validation.validate_nutrient_name(nutrient_name)
        return self._nutrient_relations[nutrient_name]

    def nutrient_ratio_matches_relation(self, nutrient_ratio: 'nutrients.NutrientRatio') -> Optional[bool]:
        """Returns True/False/None to indicate if the nutrient relation
        matches the nutrient ratio supplied."""
        # Grab the implication first;
        implication = self.get_implication_for_nutrient(nutrient_ratio.nutrient.primary_name)

        # If nutrient ratio is undefined, return None, regardless of implication;
        if nutrient_ratio.g_per_subject_g is None:
            return None

        # If implication is zero;
        if implication is flags.FlagImpliesNutrient.zero:
            if nutrient_ratio.g_per_subject_g == 0:
                return True
            elif nutrient_ratio.g_per_subject_g > 0:
                return False

        # If implication is non-zero;
        elif implication is flags.FlagImpliesNutrient.non_zero:
            if nutrient_ratio.g_per_subject_g == 0:
                return False
            elif nutrient_ratio.g_per_subject_g > 0:
                return True


