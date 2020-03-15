from typing import TYPE_CHECKING, Dict
from pydiet.injector import injector
from pyconsoleapp.console_app_component import ConsoleAppComponent
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService

_FLAG_MENU_TEMPLATE = '''Choose a flag to edit:
{}
'''
_FLAG_MENU_ITEM_TEMPLATE = '({}) - {}\n'

_FLAG_EDITOR_TEMPLATE = 'Is {} {}?  (y)/(n)\n'


class IngredientFlagEditor(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ingredient_service: 'IngredientService' = injector.inject(
            'IngredientService')
        self._current_flag_number:int = 0
        self._flag_number_map:Dict[int, str] = {}

    def run(self)->str:
        # Update the ingredient data in the window;
        self.app.set_window_text(self._ingredient_service.summarise_ingredient(
            self._ingredient_service.current_ingredient
        ))
        self.app.show_text_window()           
        # Create map between flag numbers and flag names;
        for i, flag_name in enumerate(\
            self._ingredient_service.current_ingredient.flag_data.keys(), start=1):
            self._flag_number_map[i] = flag_name
        # If there is currently no flag selected;     
        if not self._current_flag_number:
            output = ''
            # Build the flag option output;
            for option_number in self._flag_number_map.keys():
                output = output + _FLAG_MENU_ITEM_TEMPLATE.\
                    format(option_number, self._flag_number_map[option_number])     
            output = _FLAG_MENU_TEMPLATE.format(output)
            output = self.run_parent('standard_page', output)
            return output   
        else:
            output = _FLAG_EDITOR_TEMPLATE.format(
                self._ingredient_service.current_ingredient.name,
                self._flag_number_map[self._current_flag_number].replace('_', ' ')
            )
            return output

    def dynamic_response(self, response)->None:
        # If the user has just chosen a flag;
        if not self._current_flag_number:
            for flag_number in self._flag_number_map.keys():
                if str(flag_number) == response:
                    self._current_flag_number = int(response)
                    return
        # If the user has just edited a flag
        else:
            if response == 'y':
                self._ingredient_service.current_ingredient.set_flag(
                    self._flag_number_map[self._current_flag_number], True
                )
            elif response == 'n':
                self._ingredient_service.current_ingredient.set_flag(
                    self._flag_number_map[self._current_flag_number], False
                )
            self._current_flag_number = 0    



ingredient_flag_editor = IngredientFlagEditor()