from typing import Optional, List

import model


class FlagNutrientRelation:
    """Models the relationship between a flag and a nutrient."""

    def __init__(self, flag_name: str, nutrient_name: str,
                 flag_implies_nutrient_zero: Optional[bool] = None,
                 flag_implies_nutrient_non_zero: Optional[bool] = None, **kwargs):
        if len(kwargs):
            raise ValueError("FlagNutrientRelation - leftover arguments.")
        flag_name = model.flags.validation.validate_flag_name(flag_name)
        nutrient_name = model.nutrients.validation.validate_nutrient_name(nutrient_name)
        if flag_implies_nutrient_zero is None and flag_implies_nutrient_non_zero is None:
            raise ValueError(
                'Params implies_nutrient_zero and implies_nutrient_non_zero cannot both be None')
        if flag_implies_nutrient_zero == flag_implies_nutrient_non_zero:
            raise ValueError(
                'Params implies_nutrient_zero and implies_nutrient_non_zero cannot both be True or False')
        self._flag_name = flag_name
        self._nutrient_name = nutrient_name
        if flag_implies_nutrient_zero is not None:
            self._flag_implies_nutrient_zero = flag_implies_nutrient_zero
        elif flag_implies_nutrient_non_zero is not None:
            self._flag_implies_nutrient_zero = not flag_implies_nutrient_non_zero

    @property
    def flag_name(self) -> str:
        return self._flag_name

    @property
    def nutrient_name(self) -> str:
        return self._nutrient_name

    @property
    def flag_implies_nutrient_zero(self) -> bool:
        return self._flag_implies_nutrient_zero

    @property
    def flag_implies_nutrient_non_zero(self) -> bool:
        return not self._flag_implies_nutrient_zero


class FlagNutrientRelations:
    """Class to model a collection of flag-nutrient relations."""

    def __init__(self):
        self._relations: List['FlagNutrientRelation'] = []

    def add_relation(self, **kwargs):
        """Adds a flag-nutrient relation to the list.
        Keyword Args:
            flag_name (str): Name of the flag involved in the relation.
            nutrient_name (str): Name of the nutrient involved in the relation.
            flag_implies_nutrient_zero (Optional[bool]): Indicates if the flag being True implies the
                nutrient should be zero.
            flag_implies_nutrient_non_zero (Optional[bool]): Indicates if the flag being True implies the
                nutrient should be non-zero.

        Note:
            Either flag_implies_nutrient_zero OR flag_implies_nutrient_non_zero should be set. Not both. One OR
            the other *must* be set.
        """
        self._relations.append(FlagNutrientRelation(**kwargs))

    def implied_non_zero_nutrients(self, flag_name: str, flag_value: bool) -> List[str]:
        """Returns a list of nutrients which the flag implies are non-zero."""

    def implied_zero_nutrients(self, flag_name: str, flag_value: bool) -> List[str]:
        """Returns a list of nutrients which the flag implies are zero."""

    def implied_true_flags(self, nutrient_name: str, nutrient_g_per_subject_g: float) -> List[str]:
        """Returns a list of flags which the nutrient statement implies must be true."""

    def implied_false_flags(self, nutrient_name: str, nutrient_g_per_subject_g: float) -> List[str]:
        """Returns a list of flags which the nutrient statement implies must be false."""
