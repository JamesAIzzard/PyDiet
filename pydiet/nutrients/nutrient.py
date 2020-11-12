from typing import Dict, List, Optional

from pydiet import nutrients
from pydiet.nutrients import configs, global_nutrients


class Nutrient:
    def __init__(self, name: str):
        self._name = nutrients.get_nutrient_primary_name(name)
        self._parent_nutrients_cache: Optional[Dict[str, 'Nutrient']] = None
        self._child_nutrients_cache: Optional[Dict[str, 'Nutrient']] = None
        # Todo - Looking at building flag relation into nutrient here.
        self._flag_name_relations: Dict[str, ]

    @property
    def primary_name(self) -> str:
        """Returns the nutrient's primary name."""
        return self._name

    @property
    def aliases(self) -> List[str]:
        """Returns a list of aliases for the nutrient's primary name."""
        return configs.nutrient_aliases[self.primary_name]

    @property
    def calories_per_g(self) -> float:
        """Returns the calories in one gram of the nutrient."""
        if self.primary_name in configs.calorie_nutrients.keys():
            return configs.calorie_nutrients[self.primary_name]
        else:
            return 0

    @property
    def parent_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the nutrient's parents. For example, the parent of 'glucose' is 'carbohydrate'."""
        if self._parent_nutrients_cache is None:
            ng_defs = configs.nutrient_group_definitions
            glb_nuts = global_nutrients
            self._parent_nutrients_cache = {}
            for group_name in ng_defs.keys():
                if self.primary_name in ng_defs[group_name]:
                    self._parent_nutrients_cache[group_name] = glb_nuts[group_name]
        return self._parent_nutrients_cache

    @property
    def child_nutrients(self) -> Dict[str, 'Nutrient']:
        """Returns the nutrient's children. For example, a child of 'carbohydrate' is glucose."""
        if self._child_nutrients_cache is None:
            ng_defs = configs.nutrient_group_definitions
            glb_nuts = global_nutrients
            self._child_nutrients_cache = {}
            if self.primary_name in ng_defs.keys():
                for child_nut_name in ng_defs[self.primary_name]:
                    self._child_nutrients_cache[child_nut_name] = glb_nuts[child_nut_name]
        return self._child_nutrients_cache
