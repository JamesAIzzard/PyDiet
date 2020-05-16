from typing import TYPE_CHECKING, Dict, Optional, List

from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.ingredients.nutrient_amount import NutrientAmount
    from pydiet.ingredients import ingredient_service
    from pyconsoleapp import ConsoleApp
    from pydiet.shared import configs
    from pydiet.cli.shared import utility_service as cli_utility_service
#    from pydiet.cli.ingredients.ingredient_save_check_component import IngredientSaveCheckComponent


class IngredientEditService():
    def __init__(self):
        self._igs: 'ingredient_service' = inject('pydiet.ingredient_service')
        self._cf: 'configs' = inject('pydiet.configs')
        self._app: 'ConsoleApp' = inject('pydiet.cli.app')    
        self._cli_utils:'cli_utility_service' = inject('pydiet.cli.utility_service')    
        self._flag_number_name_map: Optional[Dict[int, str]] = None
        self._primary_nutrient_number_name_map: Optional[Dict[int, str]] = None
        self.ingredient: Optional['Ingredient'] = None
        self.datafile_name: Optional[str] = None
        self.temp_qty: Optional[float]
        self.temp_qty_units: Optional[str]
        self.current_flag_number: int
        self.cycling_flags: bool = False
        self.current_nutrient_amount: 'NutrientAmount'
        self.nutrient_name_search_results: List[str]
        self.ingredient_search_results: List[str]

    @property
    def flag_number_name_map(self) -> Dict[int, str]:
        # Create if not cached already;
        # (Caching is OK because same for all ingredients);
        if not self._flag_number_name_map:
            self._flag_number_name_map = \
                self._cli_utils.create_number_name_map(
                    list(self.ingredient.all_flag_data.keys()))
        # Return from cache;
        return self._flag_number_name_map

    @property
    def primary_nutrient_number_name_map(self) -> Dict[int, str]:
        # Create if not cached already;
        # (Caching is OK because same for all ingredients);
        if not self._primary_nutrient_number_name_map:
            self._primary_nutrient_number_name_map = \
                self._cli_utils.create_number_name_map(self._cf.PRIMARY_NUTRIENTS)
        #  Return from cache;
        return self._primary_nutrient_number_name_map

    @property
    def nutrient_search_result_number_name_map(self) -> Dict[int, str]:
        return self._cli_utils.create_number_name_map(self.nutrient_name_search_results)

    @property
    def ingredient_search_result_number_name_map(self) -> Dict[int, str]:
        return self._cli_utils.create_number_name_map(self.ingredient_search_results)

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
        defined_secondary_nutr_names = list(
            self.ingredient.defined_secondary_nutrients.keys())
        start_num = len(self._cf.PRIMARY_NUTRIENTS)+1
        return self._cli_utils.create_number_name_map(defined_secondary_nutr_names, start_num=start_num)

    def flag_name_from_number(self, selection_number: int) -> str:
        return self.flag_number_name_map[selection_number]

    def save_changes(self, redirect_to: Optional[str] = None) -> None:
        # Catch no ingredient;
        if not self.ingredient:
            raise AttributeError()
        # If creating ingredient for first time;
        if not self.datafile_name:
            # Create the datafile and stash the name;
            self.datafile_name = \
                self._igs.save_new_ingredient(self.ingredient)
            # Redirect to edit, now datafile exists;
            if redirect_to:
                self._app.clear_exit('home.ingredients.new')
                self._app.guard_exit('home.ingredients.edit', 'IngredientSaveCheckComponent')
                self._app.goto(redirect_to)
        # If updating an existing datafile;
        else:
            # Update the ingredient;
            self._igs.update_existing_ingredient(
                self.ingredient,
                self.datafile_name
            )
        # Confirm save;
        self._app.info_message = "Ingredient saved."
