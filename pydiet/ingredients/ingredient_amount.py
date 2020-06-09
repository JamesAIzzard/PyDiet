from typing import TYPE_CHECKING

from pydiet.ingredients import ingredient_service

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.recipes.recipe import Recipe

data_template = {
    "quantity": None,
    "quantity_units": None,
    "perc_increase": None,
    "perc_decrease": None
}

class IngredientAmount():

    def __init__(self, parent_recipe: 'Recipe', ingredient: 'Ingredient'):
        self.ingredient = ingredient
        self.parent_recipe = parent_recipe

    @property
    def name(self) -> str:
        return self.ingredient.name

    @property
    def ingredient_datafile_name(self)->str:
        return ingredient_service.convert_ingredient_name_to_datafile_name(self.name)

    @property
    def quantity(self) -> float:
        return self.parent_recipe._data['ingredients']\
            [self.ingredient_datafile_name]['quantity']

    @quantity.setter
    def quantity(self, value: float) -> None:
        self.parent_recipe._data['ingredients']\
            [self.ingredient_datafile_name]['quantity'] = value

    @property
    def quantity_units(self) -> str:
        return self.parent_recipe._data['ingredients']\
            [self.ingredient_datafile_name]['quantity_units']

    @quantity_units.setter
    def quantity_units(self, value: str) -> None:
        self.parent_recipe._data['ingredients']\
            [self.ingredient_datafile_name]['quantity_units'] = value

    @property
    def perc_increase(self) -> float:
        return self.parent_recipe._data['ingredients']\
            [self.ingredient_datafile_name]['perc_increase']

    @perc_increase.setter
    def perc_increase(self, value:float) -> None:
        self.parent_recipe._data['ingredients']\
            [self.ingredient_datafile_name]['perc_increase'] = value

    @property
    def perc_decrease(self) -> float:
        return self.parent_recipe._data['ingredients']\
            [self.ingredient_datafile_name]['perc_decrease']

    @perc_decrease.setter
    def perc_decrease(self, value:float) -> None:
        self.parent_recipe._data['ingredients']\
            [self.ingredient_datafile_name]['perc_decrease'] = value    
