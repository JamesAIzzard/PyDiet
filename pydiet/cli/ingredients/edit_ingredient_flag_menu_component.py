from typing import TYPE_CHECKING, cast

from pinjector import inject

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.ingredients import ingredient_service
    from pydiet.data import repository_service

_FLAG_MENU = '''(s) -- Save Changes

Choose a flag to edit:
{}
'''
_FLAG_MENU_ITEM = '({flag_number}) -- {flag_summary}\n'

class EditIngredientFlagMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._igs:'ingredient_service' = inject('pydiet.ingredient_service')
        self._rp:'repository_service' = inject('pydiet.repository_service')
        self.set_option_response('s', self.on_save_changes)

    def print(self):
        # Catch error if ingredient is not set;
        if not self._ies.ingredient:
            raise AttributeError
        flags_menu = ''
        for flag_number in self._ies.flag_number_name_map.keys():
            flag_summary = self._igs.summarise_flag(self._ies.ingredient, 
                self._ies.flag_name_from_number(flag_number))
            flags_menu = flags_menu + _FLAG_MENU_ITEM.format(
                flag_number=flag_number,
                flag_summary=flag_summary
            )
        output = _FLAG_MENU.format(flags_menu)
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def on_save_changes(self):
        self._ies.save_changes(redirect_to='home.ingredients.edit.flags')

    def dynamic_response(self, response):
        # Try and parse the response as an integer;
        try:
            response = int(response)
        except ValueError:
            return
        # Conversion went OK, so set flag number from response;
        if response in self._ies.flag_number_name_map.keys():
            self._ies.current_flag_number = response
        # And nav to set flag;      
        self.app.goto('.edit_flag')
