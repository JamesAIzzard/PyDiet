from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients import ingredient_edit_service as ies

_UNITS_TEMPLATE = '''
    {qty}{units} of {ingredient_name} costs 
    £__.____
     ^^^^^^^

How much does {qty}{units} of {ingredient_name}
cost?
'''

class EditIngredientCostComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()

    def print(self):
        # Build the output;
        output = _UNITS_TEMPLATE.format(\
            ingredient_name=self._ies.ingredient.name,
            qty=self._ies.temp_qty,
            units=self._ies.temp_qty_units
        )
        output = self.app.fetch_component('standard_page_component').call_print(output) + ' £'
        # Return it;
        return output

    def dynamic_response(self, response):
        # Try and convert the response into a cost value;
        cost = None
        try:
            cost = float(response)
        except ValueError:
            self.app.error_message = "Unable to parse {} as a cost. Try again."\
                .format(response)
            return
        # Catch qty data missing;
        if not self._ies.temp_qty or not self._ies.temp_qty_units:
            raise AttributeError
        # Set all the data;
        self._ies.ingredient.set_cost(
            cost, 
            self._ies.temp_qty, 
            self._ies.temp_qty_units)
        # Return to the menu;
        self.app.goto('home.ingredients.edit')