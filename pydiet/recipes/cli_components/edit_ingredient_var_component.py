from pyconsoleapp import ConsoleAppComponent, parse_tools

from pydiet.recipes import recipe_edit_service as res
from pydiet.recipes.exceptions import SaturatedPercDecreaseError

_TEMPLATE = '''Allowable variation for {ingredient_qty}{ingredient_qty_units} of {ingredient_name}:

- increase: {perc_increase}% (up to {max_qty}{ingredient_qty_units})
- decrease: {perc_decrease}% (down to {min_qty}{ingredient_qty_units})

Where * is % amount:
(i*)    -- Allowable % increase 
(d*)    -- Allowable % decrease
(enter) -- Accept values
(s)     -- Save changes

'''

class EditIngredientVarComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
        self.set_option_response('s', self.on_save)
        self.set_empty_enter_response(self.on_empty_enter)

    def run(self) -> None:
        # Redirect to recipe edit if no ingredient amount is selected;
        if not self._res.ingredient_amount:
            self.app.goto('home.recipes.edit')

    def print(self):
        ia = self._res.ingredient_amount
        # Calculate the min and max qty;
        max_qty = round(ia.quantity*(1+(ia.perc_increase/100)), 2)
        min_qty = round(ia.quantity*(1-(ia.perc_decrease/100)), 2)
        # Build the template;
        output = _TEMPLATE.format(
            ingredient_qty=ia.quantity,
            ingredient_qty_units=ia.quantity_units,
            ingredient_name=ia.name,
            perc_increase=ia.perc_increase,
            perc_decrease=ia.perc_decrease,
            max_qty=max_qty,
            min_qty=min_qty
        )
        # Format and return it;
        output = self.app.fetch_component('standard_page_component').call_print(output)
        return output

    def on_save(self):
        self._res.save_changes()

    def on_empty_enter(self):
        self.app.goto('home.recipes.edit.ingredients')

    def dynamic_response(self, raw_response: str) -> None:
        # Try parse letter and float;
        try:
            letter, number = parse_tools.parse_letter_and_float(raw_response)
        except parse_tools.LetterFloatParseError:
            return
        # If we are changing the % increase value;
        if letter == 'i':
            try:
                    self._res.ingredient_amount.perc_increase = number
            except ValueError:
                self.app.error_message = '{} is not a valid increase value.'.format(number)
                return
        # If we are changing the % decrease value;
        elif letter == 'd':
            try:
                self._res.ingredient_amount.perc_decrease = number
            except ValueError:
                self.app.error_message = '{} is not a valid decrease value.'.format(number)
            except SaturatedPercDecreaseError:
                self.app.info_message = 'The maximum decrease value of 100% has been used.'
                self._res.ingredient_amount.perc_decrease = 100