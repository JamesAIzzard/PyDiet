from typing import List, Dict


class Nutrient:
    def __init__(self, nutrient_name: str, alias_names: List[str], calories_per_g: float,
                 direct_child_nutrient_names: List[str],
                 direct_parent_nutrient_names: List[str],
                 all_sibling_nutrient_names: List[str],
                 all_descendant_nutrient_names: List[str],
                 all_ascendant_nutrient_names: List[str],
                 all_relative_nutrient_names: List[str],
                 global_nutrients: Dict[str, 'Nutrient']):

        self._name: str = nutrient_name
        self._alias_names: List[str] = alias_names
        self._calories_per_g: float = calories_per_g

        self._global_nutrients = global_nutrients

        # These next values are populated by the nutrient factory function during the
        # nutrient tree initialisation process;
        self._direct_child_nutrient_names: List[str] = direct_child_nutrient_names
        self._direct_parent_nutrient_names: List[str] = direct_parent_nutrient_names
        self._all_sibling_nutrient_names: List[str] = all_sibling_nutrient_names
        self._all_descendant_nutrient_names: List[str] = all_descendant_nutrient_names
        self._all_ascendant_nutrient_names: List[str] = all_ascendant_nutrient_names
        self._all_relative_nutrient_names: List[str] = all_relative_nutrient_names

    @property
    def primary_name(self) -> str:
        """Returns the nutrient's primary name."""
        return self._name

    @property
    def direct_child_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of the nutrient's direct children, or an empty list if there are none."""
        return dict((k, self._global_nutrients[k]) for k in self._direct_child_nutrient_names if k in self._global_nutrients)

    @property
    def direct_parent_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of the nutrient's direct parents, or an empty list if there are none."""
        return dict((k, self._global_nutrients[k]) for k in self._direct_parent_nutrient_names if k in self._global_nutrients)

    @property
    def all_sibling_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of the nutrient's siblings, or an empty list if there are none."""
        return dict((k, self._global_nutrients[k]) for k in self._direct_parent_nutrient_names if k in self._global_nutrients)

    @property
    def all_ascendant_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of all ascendants to this nutrient, or an empty list if there are none."""
        return dict((k, self._global_nutrients[k]) for k in self._all_ascendant_nutrient_names if k in self._global_nutrients)

    @property
    def all_descendant_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of all descendants of this nutrient, or an empty list if there are none."""
        return dict((k, self._global_nutrients[k]) for k in self._all_descendant_nutrient_names if k in self._global_nutrients)

    @property
    def all_relative_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the names of all relatives to this nutrient, or an empty list if there are none."""
        return dict((k, self._global_nutrients[k]) for k in self._all_relative_nutrient_names if k in self._global_nutrients)

    @property
    def alias_names(self) -> List[str]:
        """Returns a list of aliases for the nutrient's primary name."""
        return self._alias_names

    @property
    def calories_per_g(self) -> float:
        """Returns the calories in one gram of the nutrient."""
        return self._calories_per_g
