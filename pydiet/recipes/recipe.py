from typing import TYPE_CHECKING, Dict, List

from pydiet.recipes.exceptions import DuplicateRecipeNameError
from pydiet.recipes import recipe_service as rcs
from pydiet.shared import utility_service as uts

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_amount import IngredientAmount

class Recipe():

    def __init__(self, data_template: Dict):
        self._data: Dict = data_template
        self._ingredient_amounts: Dict[str, 'IngredientAmount'] = {}
        self.categories: List[str] = []

    @property
    def name(self) -> str:
        return self._data['name']

    @name.setter
    def name(self, name: str) -> None:
        if rcs.recipe_name_used(name):
            raise DuplicateRecipeNameError
        else:
            self._data['name'] = name

    @property
    def serve_intervals(self) -> List[str]:
        return self._data['serve_intervals']

    def add_serve_interval(self, serve_interval:str) -> None:
        # Check the serve interval is valid;
        serve_interval = uts.parse_time_interval(serve_interval)
        # If it isn't already there;
        if not serve_interval in self.serve_intervals:
            # Assign it;
            self._data['serve_intervals'].append(serve_interval)

    def remove_serve_interval(self, serve_interval:str) -> None:
        # Cycle through the serve intervals
        for se in self.serve_intervals:
            # Remove matchign one if found;
            if se == serve_interval:
                self._data['serve_between'].pop(serve_interval)

    def clear_serve_intervals(self):
        # Clear all;
        self._data['serve_between'] = []

    @property
    def ingredient_amounts(self)->Dict[str, 'IngredientAmount']:
        return self._ingredient_amounts

