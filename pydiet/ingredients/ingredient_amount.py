from typing import TYPE_CHECKING

from pydiet.ingredients import ingredient_service
from pydiet import units as unt
from pydiet.ingredients.exceptions import IngredientDensityUndefinedError
from pydiet.recipes.exceptions import SaturatedPercDecreaseError

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.recipes.recipe import Recipe

data_template = {
    "quantity": None,
    "quantity_units": None,
    "perc_increase": 0,
    "perc_decrease": 0
}


class IngredientAmount():

    def __init__(self, parent_recipe: 'Recipe', ingredient: 'Ingredient'):
        self.ingredient = ingredient
        self.parent_recipe = parent_recipe

    @property
    def name(self) -> str:
        return self.ingredient.name

    @property
    def ingredient_datafile_name(self) -> str:
        return ingredient_service.convert_ingredient_name_to_datafile_name(self.name)

    @property
    def quantity(self) -> float:
        return self.parent_recipe._data['ingredients'][self.ingredient_datafile_name]['quantity']

    @property
    def quantity_units(self) -> str:
        return self.parent_recipe._data['ingredients'][self.ingredient_datafile_name]['quantity_units']

    def set_quantity_and_units(self, quantity: float, units: str) -> None:
        '''Set the quantity and units of the named ingredient amount.

        Args:
            quantity (float): Nominal quantity of the ingredient required.
            units (str): Units of the quantity provided.

        Raises:
            ValueError: The quantity value provided is not suitable.
            IngredientDensityUndefinedError: The units are volumetric and
                volumentrics are not configured on the ingredient.
        '''
        # Check the quantity value;
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError
        # Check the units;
        units = unt.parse_qty_unit(units)
        # If the unit is volumetric, check the ingredient has density configured;
        if units in unt.recognised_vol_units() and not self.ingredient.density_is_defined:
            raise IngredientDensityUndefinedError
        # All is OK, go ahead and set;
        self.parent_recipe._data['ingredients'][self.ingredient_datafile_name]['quantity'] = quantity
        self.parent_recipe._data['ingredients'][self.ingredient_datafile_name]['quantity_units'] = units

    @property
    def perc_increase(self) -> float:
        return self.parent_recipe._data['ingredients'][self.ingredient_datafile_name]['perc_increase']

    @perc_increase.setter
    def perc_increase(self, value: float) -> None:
        '''Sets the allowable percentage increase.

        Args:
            value (float): The allowable % increase.

        Raises:
            ValueError: The value provided is not suitable.
        '''
        # Check the value is OK;
        perc_increase = float(value)
        if perc_increase < 0:
            raise ValueError
        # Write the value;
        self.parent_recipe._data['ingredients'][self.ingredient_datafile_name]['perc_increase'] = perc_increase

    @property
    def perc_decrease(self) -> float:
        return self.parent_recipe._data['ingredients'][self.ingredient_datafile_name]['perc_decrease']

    @perc_decrease.setter
    def perc_decrease(self, value: float) -> None:
        '''Sets the allowable percentage decrease.

        Args:
            value (float): The allowable % decrease.

        Raises:
            ValueError: The value provided is not suitable.
        '''
        # Check the value is OK;
        perc_decrease = float(value)
        if perc_decrease < 0:
            raise ValueError
        if perc_decrease > 100:
            raise SaturatedPercDecreaseError
        # Write the value;
        self.parent_recipe._data['ingredients'][self.ingredient_datafile_name]['perc_decrease'] = perc_decrease

    @property
    def max_quantity(self) -> float:
        return self.quantity*(1+(self.perc_increase/100))

    @property
    def min_quantity(self) -> float:
        return self.quantity*(1-(self.perc_decrease/100))
