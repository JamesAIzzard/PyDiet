from typing import Dict, List

from pydiet import nutrients


class Nutrient:
    def __init__(self, name: str):
        self._name = nutrients.nutrients_service.get_nutrient_primary_name(
            name)
        self._parent_nutrients: Dict[str, Nutrient] = {}
        self._child_nutrients: Dict[str, Nutrient] = {}

        # Init any child nutrients;
        if self.primary_name in nutrients.configs.nutrient_group_definitions:
            for child_name in nutrients.configs.nutrient_group_definitions[self.primary_name]:
                # If the child nutrient already instantiated, add to list;
                if child_name in nutrients.global_nutrients:
                    self._child_nutrients[child_name] = nutrients.global_nutrients[child_name]
                # Otherwise instanitate;
                nutrients.global_nutrients[child_name] = Nutrient(child_name)
                self._child_nutrients[child_name] = nutrients.global_nutrients[child_name]

        # Init any parent nutrients;
        for parent_name in nutrients.configs.nutrient_group_definitions:
            # If my name shows up as a child in any groups;
            if self.primary_name in nutrients.configs.nutrient_group_definitions[parent_name]:
                # If the parent nutrient already instantiated, add to list;
                if parent_name in nutrients.global_nutrients:
                    self._parent_nutrients[parent_name] = nutrients.global_nutrients[parent_name]
                # Otherwise instantiate;
                nutrients.global_nutrients[parent_name] = Nutrient(parent_name)
                self._parent_nutrients[parent_name] = nutrients.global_nutrients[parent_name]

    @property
    def primary_name(self) -> str:
        return self._name

    @property
    def aliases(self) -> List[str]:
        raise NotImplementedError

    @property
    def calories_per_g(self) -> float:
        if self.primary_name in nutrients.configs.calorie_nutrients.keys():
            return nutrients.configs.calorie_nutrients[self.primary_name]
        else:
            return 0

    @property
    def parent_nutrients(self) -> Dict[str, 'Nutrient']:
        return self._parent_nutrients

    @property
    def child_nutrients(self) -> Dict[str, 'Nutrient']:
        return self._child_nutrients
