from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs


_TEMPLATE = '\nIs {ingredient_name} {flag}?  (y)/(n)\n\n'


class EditIngredientFlagComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()
        self.set_option_response('y', self.on_yes)
        self.set_option_response('n', self.on_no)

    def print(self):
        output = _TEMPLATE.format(
            ingredient_name=self._ies.ingredient.name.lower(),
            flag=self._ies.flag_name_from_number(self._ies.current_flag_number)
        ).replace('_', ' ')
        output = self.app.fetch_component('standard_page_component').call_print(output)
        return output

    def on_yes(self):
        # Update the flag on the ingredient;
        self._ies.ingredient.set_flag(self._ies.current_flag_name, True)
        # Handover;
        self.after_flag_set()

    def on_no(self):
        # Update the flag on the ingredient;
        self._ies.ingredient.set_flag(self._ies.current_flag_name, False)
        # Handover;
        self.after_flag_set()
    
    def after_flag_set(self):
        # If we are cycling flags;
        if self._ies.cycling_flags:
            # If we havent got to the end yet;
            if not self._ies.last_flag_selected:
                self._ies.current_flag_number = self._ies.current_flag_number + 1
                return
            # We have got to the end;
            else:
                self._ies.cycling_flags = False
                self._ies.current_flag_number = 0
                self.app.info_message = 'All flags were set.'
                self.app.goto('home.ingredients.edit.flags')
        # Not cycling flags;
        else:
            # Just reset state and go back;
            self._ies.current_flag_number = 0
            self.app.goto('home.ingredients.edit.flags')

