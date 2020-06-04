from typing import TYPE_CHECKING, Dict, List

from pydiet.recipes.exceptions import DuplicateRecipeNameError
from pydiet.recipes import recipe_service as rcs
from pydiet import configs
from pydiet.recipes.exceptions import (
    UnknownTagError
)

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_amount import IngredientAmount


class Recipe():

    def __init__(self, data_template: Dict):
        self._data: Dict = data_template
        self._ingredient_amounts: Dict[str, 'IngredientAmount'] = {}

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
    def tags(self) -> List[str]:
        return self._data['tags']

    def add_tag(self, tag:str) -> None:
        # Check that the tag is on the list in configs;
        if not tag in configs.RECIPE_TAGS:
            raise UnknownTagError
        # If the tag is not already on the list;
        if not tag in self.tags:
            self._data['tags'].append(tag)

    def remove_tag(self, tag:str) -> None:
        # If the tag is in the list;
        if tag in self.tags:
            # Remove it;
            self._data['tags'].remove(tag)

    @property
    def serve_intervals(self) -> List[str]:
        return self._data['serve_intervals']

    def update_serve_interval(self, new_serve_interval:str, index:int)->None:
        # Validate the time interval;
        new_serve_interval = rcs.parse_time_interval(new_serve_interval)
        # Overwrite the specified index;
        self._data['serve_intervals'][index] = new_serve_interval


    def add_serve_interval(self, serve_interval: str) -> None:
        # Check the serve interval is valid;
        serve_interval = rcs.parse_time_interval(serve_interval)
        # If it isn't already there;
        if not serve_interval in self.serve_intervals:
            # Assign it;
            self._data['serve_intervals'].append(serve_interval)

    def remove_serve_interval(self, serve_interval: str) -> None:
        # Cycle through the serve intervals
        for se in self.serve_intervals:
            # Remove matchign one if found;
            if se == serve_interval:
                self._data['serve_intervals'].pop(serve_interval)

    def clear_serve_intervals(self):
        # Clear all;
        self._data['serve_between'] = []

    @property
    def ingredient_amounts(self) -> Dict[str, 'IngredientAmount']:
        return self._ingredient_amounts
