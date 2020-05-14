from typing import TYPE_CHECKING, Dict, List

from pinjector import inject

from pydiet.recipes.exceptions import DuplicateRecipeNameError

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_amount import IngredientAmount
    from pydiet.recipes import recipe_service
    from pydiet.shared import utility_service

class Recipe():

    def __init__(self, data_template: Dict):
        self._rcs: 'recipe_service' = inject('pydiet.recipe_service')
        self._ut: 'utility_service' = inject('pydiet.utility_service')
        self._data: Dict = data_template
        self.ingredient_amounts: Dict[str, 'IngredientAmount']
        self.categories: List[str]

    @property
    def name(self) -> str:
        return self._data['name']

    @name.setter
    def name(self, name: str) -> None:
        if self._rcs.recipe_name_used(name):
            raise DuplicateRecipeNameError
        else:
            self._data['name'] = name

    @property
    def serve_intervals(self) -> List[str]:
        return self._data['serve_between']

    def add_serve_interval(self, serve_interval:str) -> None:
        # Check the serve interval is valid;
        serve_interval = self._ut.parse_time_interval(serve_interval)
        # If it isn't already there;
        if not serve_interval in self.serve_intervals:
            # Assign it;
            self._data['serve_between'].append(serve_interval)

    def remove_serve_interval(self, serve_interval:str) -> None:
        # Cycle through the serve intervals
        for se in self.serve_intervals:
            # Remove matchign one if found;
            if se == serve_interval:
                self._data['serve_between'].pop(serve_interval)

    def clear_serve_intervals(self):
        # Clear all;
        self._data['serve_between'] = []

