from pyconsoleapp import ConsoleAppComponent

from pydiet.cli.ingredients import ingredient_edit_service as ies
from pydiet.shared import utility_service as uts

from pydiet.ingredients.exceptions import (
    ConstituentsExceedGroupError, FlagNutrientConflictError,
    NutrientQtyExceedsIngredientQtyError
)
from pydiet.shared.exceptions import UnknownUnitError

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


class EditIngredientNutrientMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ies = ies.IngredientEditService()

    def print(self):
        output = _NUTRIENT_MASS.format(
            ingredient_name=self._ies.ingredient.name.lower(),
            nutrient_name=self._ies.current_nutrient_amount.name,
            qty=self._ies.temp_qty,
            units=self._ies.temp_qty_units,
            valid_units=uts.recognised_mass_units()
        )
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            mass, units = uts.parse_number_and_text(response)
        # Catch parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a qty & unit. Try again."\
                .format(response)
            return
        # Parse unit to correct case;
        try:
            units = uts.parse_mass_unit(units)
        # Catch unknown units;
        except UnknownUnitError:
            self.app.error_message = "{} is not a recognised mass unit.".format(
                units)
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
        except FlagNutrientConflictError:
            self.app.info_message = 'Flag status updated to correspond with {} quantity'.format(
                self._ies.current_nutrient_amount.name)
        # Navigate back to the nutrient menu;
        self.app.goto('home.ingredients.edit.nutrients')
