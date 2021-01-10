from pyconsoleapp import ConsoleAppComponent, parse_tools

from pydiet.recipes import recipe_edit_service as res
from pydiet.ingredients.exceptions import IngredientDensityUndefinedError
from pydiet import units as unt

_TEMPLATE = '''How much {ingredient_name} is there in the {recipe_name} recipe?
(e.g 100g, 20L 0.5kg etc.)

'''


class EditIngredientQtyComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()

    def print(self):
        output = _TEMPLATE.format(
            ingredient_name=self._res.ingredient_amount.name,
            recipe_name=self._res.recipe.name
        )
        output = self.app.fetch_component(
            'standard_page_component').call_print(output)
        return output

    def dynamic_response(self, raw_response: str) -> None:
        # Check an ingredient is selected;
        if not self._res.ingredient_amount:
            raise AttributeError
        # Try and split the response into a mass and a unit;
        try:
            qty, unit = parse_tools.parse_number_and_text(raw_response)
            unit = unt.parse_qty_unit(unit)
        except parse_tools.NumberAndTextParseError:
            self.app.error_message = 'Unable to parse {} as a quantity and unit'.format(
                raw_response)
            return
        # Try set the ingredient qty;
        try:
            self._res.ingredient_amount.set_quantity_and_units(qty, unit)
        except ValueError:
            self.app.error_message = 'The ingredient quantity must be a positive number > 0.'
        except unt.UnknownUnitError:
            self.app.error_message = 'Unable to parse {} as a quantity and a recognised unit'.format(
                raw_response)            
        except IngredientDensityUndefinedError:
            self.app.info_message = 'Volumetric measurements must be configured for {ingredient_name} before it can be measured in {unit}'.format(
                ingredient_name=self._res.ingredient_amount.name,
                unit=unit
            )
            return            
        # Back to the ingredient amount menu;
        self.app.goto('home.recipes.edit.ingredients')
