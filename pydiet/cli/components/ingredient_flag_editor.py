from typing import Optional, TYPE_CHECKING, Dict
from pinjector.injector import injector
from pyconsoleapp.console_app_component import ConsoleAppComponent
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService

_FLAG_MENU = '''Choose a flag to edit:
{}
'''
_FLAG_MENU_ITEM = '({flag_number}) - {flag}\n'
_FLAG_EDITOR = '\nIs {ingredient_name} {flag}?  (y)/(n)\n\n'
_SET_ALL_FLAGS_QUESTION = '\nSet all flags now? (y)/(n)\n\n'
_FLAGS_SET_CONFIRMATION = '''\nAll flags are set!
        (o)k.\n
'''


class IngredientFlagEditor(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ingredient_service: 'IngredientService' = injector.inject(
            'IngredientService')
        self._current_flag_number: int = 0
        self._flag_number_map: Dict[str, str] = {}
        self._cycling: bool
        self._state: str

    def reset(self):
        self._build_flag_number_map()
        self._current_flag_number = 1
        self._asked_cycle = False
        # Initialise the state;
        # Ask if the user wants to cycle through the flags if they are all unset;
        if self._ingredient_service.current_ingredient.all_flags_undefined:
            self._state = 'asking_to_cycle'
        # Otherwise just show them the flag menu;
        else:
            self._state = 'showing_flag_menu'

    def _build_flag_number_map(self) -> None:
        # Create map between flag numbers and flag names;
        for i, flag_name in enumerate(
                self._ingredient_service.current_ingredient.flag_data.keys(), start=1):
            self._flag_number_map[str(i)] = flag_name

    def run(self) -> str:
        # Check current ingredient is set;
        if not self._ingredient_service.current_ingredient:
            raise NameError('The current ingredient is not defined.')
        # Update the ingredient data in the window;
        self.app.set_window_text(self._ingredient_service.summarise_ingredient(
            self._ingredient_service.current_ingredient
        ))
        self.app.show_text_window()
        # Prepare a string to hold the output;
        output = ''
        # Go for it!;
        # If we need to ask the user if they want to cycle;
        if self._state == 'asking_to_cycle':
            output = _SET_ALL_FLAGS_QUESTION
        # If we need to show the user the flag menu;
        elif self._state == 'showing_flag_menu':
            for option_number in self._flag_number_map.keys():
                output = output + _FLAG_MENU_ITEM.\
                    format(
                        flag_number=option_number,
                        flag=self._flag_number_map[option_number]
                    )
            output = _FLAG_MENU.format(output)
        # If we need to ask the user about a particular flag;
        elif self._state == 'setting_flag':
            output = _FLAG_EDITOR.format(
                ingredient_name=self._ingredient_service.current_ingredient.name,
                flag=self._flag_number_map[str(self._current_flag_number)]
            )
        # If we need to tell the user they have cycled through
        # all the flags;
        elif self._state == 'saying_cycle_finished':
            output = _FLAGS_SET_CONFIRMATION
        # Wrap the output in the standard page & return;
        output = self.run_parent('StandardPage', output)
        return output

    def dynamic_response(self, response) -> None:
        # If the user has just been asked if they want to cycle
        # through the flags;
        if self._state == 'asking_to_cycle':
            if response == 'y':
                self._cycling = True
                self._state = 'setting_flag'
            elif response == 'n':
                self._cycling = False
                self._state = 'showing_flag_menu'
        # If the user has just been shown the flag menu;
        elif self._state == 'showing_flag_menu':
            if response in self._flag_number_map.keys():
                self._current_flag_number = response
                self._state = 'setting_flag'
        # If the user has just been asked about a specific flag;
        elif self._state == 'setting_flag':
            if response == 'y':
                self._ingredient_service.current_ingredient.set_flag(
                    self._flag_number_map[str(self._current_flag_number)],
                    True
                )
            elif response == 'n':
                self._ingredient_service.current_ingredient.set_flag(
                    self._flag_number_map[str(self._current_flag_number)],
                    False
                )
            if self._cycling:
                if self._current_flag_number < len(self._flag_number_map):
                    self._current_flag_number = self._current_flag_number + 1
                else:
                    self._state = 'saying_cycle_finished'
            else:
                self._state = 'showing_flag_menu'
        # If the user has just been told the cycle has finished;
        elif self._state == 'saying_cycle_finished':
            self._state = 'showing_flag_menu'
            self._cycling = False

