from typing import TYPE_CHECKING, Dict, Optional, List

from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient, NutrientAmount
    from pyconsoleapp import ConsoleApp
    from pydiet.shared import configs


class IngredientEditService():
    def __init__(self):
        self._cf: 'configs' = inject('pydiet.configs')
        self._flag_number_name_map: Optional[Dict[int, str]] = None
        self._primary_nutrient_number_name_map: Optional[Dict[int, str]] = None
        self.ingredient: 'Ingredient'
        self.app: 'ConsoleApp' = inject('pydiet.cli.app')
        self.temp_cost_mass: float
        self.temp_cost_mass_units: str
        self.temp_volume: Optional[float]
        self.temp_volume_units: Optional[str]
        self.current_flag_number: int
        self.cycling_flags: bool = False
        self.temp_nutrient_ingredient_mass: float
        self.temp_nutrient_ingredient_mass_units: str
        self.current_nutrient_amount: 'NutrientAmount'
        self.nutrient_name_search_results: List[str]

    @property
    def flag_number_name_map(self) -> Dict[int, str]:
        # Create if not cached already;
        # (Caching is OK because same for all ingredients);
        if not self._flag_number_name_map:
            self._flag_number_name_map = \
                self._create_number_name_map(
                    list(self.ingredient.all_flag_data.keys()))
        # Return from cache;
        return self._flag_number_name_map

    @property
    def primary_nutrient_number_name_map(self) -> Dict[int, str]:
        # Create if not cached already;
        # (Caching is OK because same for all ingredients);
        if not self._primary_nutrient_number_name_map:
            self._primary_nutrient_number_name_map = \
                self._create_number_name_map(self._cf.PRIMARY_NUTRIENTS)
        #  Return from cache;
        return self._primary_nutrient_number_name_map

    @property
    def nutrient_search_result_number_name_map(self) -> Dict[int, str]:
        return self._create_number_name_map(self.nutrient_name_search_results)

    @property
    def current_flag_name(self) -> str:
        return self.flag_name_from_number(self.current_flag_number)

    @property
    def last_flag_selected(self) -> bool:
        if self.current_flag_number < len(self.flag_number_name_map):
            return False
        else:
            return True

    @property
    def defined_secondary_nutrient_number_name_map(self) -> Dict[int, str]:
        defined_secondary_nutr_names = list(self.ingredient.defined_secondary_nutrients.keys())
        start_num = len(self._cf.PRIMARY_NUTRIENTS)+1
        return self._create_number_name_map(defined_secondary_nutr_names, start_num=start_num)

    def _create_number_name_map(self, list_to_map: List, start_num=1) -> Dict[int, str]:
        map: Dict[int, str] = {}
        for i, key in enumerate(list_to_map, start=start_num):
            map[i] = key
        return map

    def flag_name_from_number(self, selection_number: int) -> str:
        return self.flag_number_name_map[selection_number]
