from typing import TYPE_CHECKING, cast

from pinjector import inject

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.cli.ingredients.ingredient_save_check_component import IngredientSaveCheckComponent
    from pydiet.ingredients import ingredient_service
    from pydiet.data import repository_service

_FLAG_MENU = '''(s) -- Save Changes

Choose a flag to edit:
{}
'''
_FLAG_MENU_ITEM = '({flag_number}) -- {flag_summary}\n'

class EditFlagMenuComponent(ConsoleAppComponent):

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
        output = self.get_component('standard_page_component').print(output)
        return output

    def on_save_changes(self):
        # Catch no ingredient;
        if not self._ies.ingredient:
            raise AttributeError()
        # If creating ingredient for first time;
        if not self._ies.datafile_name:
            # Create the datafile and stash the name;
            self._ies.datafile_name = \
                self._rp.create_ingredient(self._ies.ingredient)
            # Redirect to edit, now datafile exists;
            self.clear_exit('home.ingredients.new')
            save_check_comp = cast('IngredientSaveCheckComponent', self.get_component('ingredient_save_check_component'))
            save_check_comp.guarded_route = 'home.ingredients.edit'
            self.guard_exit('home.ingredients.edit', 'ingredient_save_check_component')
            self.goto('home.ingredients.edit.flags')
        # If updating an existing datafile;
        else:
            # Update the ingredient;
            self._rp.update_ingredient(
                self._ies.ingredient, 
                self._ies.datafile_name
            )
        # Confirm save and return;
        self.app.info_message = "Ingredient saved."
        return

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
        self.goto('.edit_flag')
