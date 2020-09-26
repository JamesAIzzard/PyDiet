from typing import Dict, List, Optional

from pydiet import nutrients


class Nutrient:
    def __init__(self, name: str):
        self._name = nutrients.nutrients_service.get_nutrient_primary_name(name)
        self._parent_nutrients_cache: Optional[Dict[str, 'Nutrient']] = None
        self._child_nutrients_cache: Optional[Dict[str, 'Nutrient']] = None

    @property
    def primary_name(self) -> str:
        return self._name

    @property
    def aliases(self) -> List[str]:
        return nutrients.configs.nutrient_aliases[self.primary_name]

    @property
    def calories_per_g(self) -> float:
        if self.primary_name in nutrients.configs.calorie_nutrients.keys():
            return nutrients.configs.calorie_nutrients[self.primary_name]
        else:
            return 0

    @property
    def parent_nutrients(self) -> Dict[str, 'Nutrient']:
        if self._parent_nutrients_cache is None:
            ng_defs = nutrients.configs.nutrient_group_definitions
            glb_nuts = nutrients.global_nutrients
            self._parent_nutrients_cache = {}
            for group_name in ng_defs.keys():
                if self.primary_name in ng_defs[group_name]:
                    self._parent_nutrients_cache[group_name] = glb_nuts[group_name]
        return self._parent_nutrients_cache

    @property
    def child_nutrients(self) -> Dict[str, 'Nutrient']:
        if self._child_nutrients_cache is None:
            ng_defs = nutrients.configs.nutrient_group_definitions
            glb_nuts = nutrients.global_nutrients
            self._child_nutrients_cache = {}
            if self.primary_name in ng_defs.keys():
                for child_nut_name in ng_defs[self.primary_name]:
                    self._child_nutrients_cache[child_nut_name] = glb_nuts[child_nut_name]
        return self._child_nutrients_cache
