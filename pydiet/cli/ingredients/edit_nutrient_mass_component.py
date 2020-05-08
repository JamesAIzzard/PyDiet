from pydiet.shared.utility_service import recognised_mass_units
from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients.exceptions import (
    ConstituentsExceedGroupError,
    NutrientQtyExceedsIngredientQtyError
)
from pydiet.shared.exceptions import UnknownUnitError

if TYPE_CHECKING:
    from pydiet.shared import utility_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_NUTRIENT_MASS = '''
    In {qty}{units} of {ingredient_name} there is

    ______ of {nutrient_name}
    ^^^^^^
Enter the weight and units of {nutrient_name}
present in {qty}{units} of {ingredient_name}.
(e.g 100g or 1kg, etc.)

Valid units:
{valid_units}

'''


class EditNutrientMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._us: 'utility_service' = inject('pydiet.utility_service')
        self._ies: 'IngredientEditService' = inject(
            'pydiet.cli.ingredient_edit_service')

    def print(self):
        output = _NUTRIENT_MASS.format(
            ingredient_name=self._ies.ingredient.name.lower(),
            nutrient_name=self._ies.current_nutrient_amount.name,
            qty=self._ies.temp_qty,
            units=self._ies.temp_qty_units,
            valid_units=self._us.recognised_mass_units()
        )
        output = self.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            mass, units = self._us.parse_number_and_text(response)
        # Catch parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a qty & unit. Try again."\
                .format(response)
            return
        # Parse unit to correct case;
        try:
            units = self._us.parse_mass_unit(units)
        # Catch unknown units;
        except UnknownUnitError:
            self.app.error_message = "{} is not a recognised mass unit.".format(units)
            return  
        # Catch unset qty and units on ies;
        if not self._ies.temp_qty or not self._ies.temp_qty_units:
            raise AttributeError
        # Try write the nutrient data to the ingredient;
        try:
            self._ies.ingredient.set_nutrient_amount(
                self._ies.current_nutrient_amount.name,
                self._ies.temp_qty,
                self._ies.temp_qty_units,
                mass,
                units
            )
        except (ConstituentsExceedGroupError, NutrientQtyExceedsIngredientQtyError) as err:
            self.app.error_message = (str(err))
            return
        except UnknownUnitError as err:
            self.app.error_message = "{} is not a recognised unit.".format(
                units)
            return
        # Navigate back to the nutrient menu;
        self.goto('..')
