from typing import TYPE_CHECKING, Dict, Optional, List

from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.ingredients import ingredient_service
    from pyconsoleapp import ConsoleApp


class IngredientEditService():
    def __init__(self):
        self._flag_number_name_map: Optional[Dict[int, str]] = None
        self.ingredient: 'Ingredient'
        self.app: 'ConsoleApp' = inject('pydiet.cli.app')
        self.temp_cost_mass: float
        self.temp_cost_mass_units: str
        self.current_flag_number: int
        self.cycling_flags: bool = False
        self.temp_nutrient_ingredient_mass: float
        self.temp_nutrient_ingredient_mass_units: str
        self.nutrient_name_search_results: List[str]

    @property
    def flag_number_name_map(self) -> Dict[int, str]:
        # Create if not cached already;
        # (Caching is OK because same for all ingredients);
        if not self._flag_number_name_map:
            self._flag_number_name_map = \
                self._create_number_name_map(self.ingredient.all_flag_data)
        # Return from cache;
        return self._flag_number_name_map

    @property
    def current_flag_name(self)->str:
        return self.flag_name_from_number(self.current_flag_number)

    @property
    def last_flag_selected(self) -> bool:
        if self.current_flag_number < len(self.flag_number_name_map):
            return False
        else:
            return True

    def _create_number_name_map(self, dict_to_map: Dict) -> Dict[int, str]:
        map: Dict[int, str] = {}
        for i, key in enumerate(dict_to_map.keys(), start=1):
            map[i] = key
        return map

    def flag_name_from_number(self, selection_number: int) -> str:
        return self.flag_number_name_map[selection_number]

    # def nutrient_name_from_number(self, selection_number: int) -> str:
    #     return self.current_nutrient_number_name_map[selection_number]

    # @property
    # def current_nutrient_number_name_map(self) -> Dict[int, str]:
    #     # Determine this dynamically because the current nutrient
    #     # group could change;
    #     return self._create_number_name_map(self.ingredient.
    #                                         _data[self.current_nutrient_group])

    # @property
    # def current_nutrient_name(self) -> str:
    #     return self.current_nutrient_number_name_map[self.current_nutrient_number]