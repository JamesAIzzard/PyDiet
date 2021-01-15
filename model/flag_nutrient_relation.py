import enum
from typing import List, TypedDict, Dict, Optional

import model


class ImpliesNutrientIs(enum.Enum):
    NON_ZERO = 1
    ZERO = 0


class FlagNutrientRelData(TypedDict):
    flag_name: str
    nutrient_name: str
    implies_nutrient_is: ImpliesNutrientIs


class FlagNutrientRelation:
    """Models the relationship between a flag and a nutrient."""

    def __init__(self, flag_name: str, nutrient_name: str, implies_nutrient_is: 'ImpliesNutrientIs'):
        self._flag_name = model.flags.validation.validate_flag_name(flag_name)
        self._nutrient_name = model.nutrients.validation.validate_nutrient_name(nutrient_name)
        self._implies_nutrient_is = implies_nutrient_is

    @property
    def flag_name(self) -> str:
        return self._flag_name

    @property
    def nutrient_name(self) -> str:
        return self._nutrient_name

    @property
    def flag_implies_nutrient_zero(self) -> bool:
        return self._implies_nutrient_is == ImpliesNutrientIs.ZERO

    @property
    def flag_implies_nutrient_non_zero(self) -> bool:
        return self._implies_nutrient_is == ImpliesNutrientIs.NON_ZERO


class FlagNutrientRelations:
    """Class to model a collection of flag-nutrient relations."""

    def __init__(self, flag_nutr_rel_data: List['FlagNutrientRelData']):
        # Maps to reference the objects from either direction;
        self._nutrient_name_map: Dict[str, List['FlagNutrientRelation']]
        self._flag_name_map: Dict[str, List['FlagNutrientRelation']]
        # Add relation objects to maps;
        for line in flag_nutr_rel_data:
            flag_name = line['flag_name']
            nutrient_name = line['nutrient_name']
            relation = FlagNutrientRelation(flag_name=flag_name,
                                            nutrient_name=nutrient_name,
                                            implies_nutrient_is=line['implies_nutrient_is'])
            self._nutrient_name_map[nutrient_name].append(relation)
            self._flag_name_map[flag_name].append(relation)

    def get_relations(self, flag_name: Optional[str], nutrient_name: Optional[str]) -> List['FlagNutrientRelation']:
        """Returns the relations associated with either the flag name or the nutrient name."""

    def implied_non_zero_nutrients(self, flag_name: str, flag_value: bool) -> List[str]:
        """Returns a list of nutrients which the flag implies are non-zero."""

    def implied_zero_nutrients(self, flag_name: str, flag_value: bool) -> List[str]:
        """Returns a list of nutrients which the flag implies are zero."""

    def implied_true_flags(self, nutrient_name: str, nutrient_g_per_subject_g: float) -> List[str]:
        """Returns a list of flags which the nutrient statement implies must be true."""

    def implied_false_flags(self, nutrient_name: str, nutrient_g_per_subject_g: float) -> List[str]:
        """Returns a list of flags which the nutrient statement implies must be false."""
