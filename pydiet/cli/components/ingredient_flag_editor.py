from typing import Optional, TYPE_CHECKING, Dict
from pinjector.injector import injector
from pyconsoleapp.console_app_component import ConsoleAppComponent
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService

_FLAG_MENU = '''Choose a flag to edit:
{}
'''
_FLAG_MENU_ITEM = '({flag_number}) - {flag}\n'
_FLAG_EDITOR = 'Is {ingredient_name} {flag}?  (y)/(n)\n'
_SET_ALL_FLAGS_QUESTION = 'Set all flags now? (y)/(n)'
_FLAGS_SET_CONFIRMATION = '''All flags are set!
        (o)k.
'''


class IngredientFlagEditor(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ingredient_service: 'IngredientService' = injector.inject(
            'IngredientService')
        self._current_flag_number: int = 0
        self._flag_number_map: Dict[int, str] = {}
        self._build_flag_number_map()
        self._cycling: bool
        self._asked_cycle: bool = False
        self._state: str

    def reset(self):
        self._current_flag_number = 0
        self._asked_cycle = False

    @property
    def _needs_name_set(self) -> bool:
        if not self._ingredient_service.current_ingredient.name:
            return True
        else:
            return False

    def _build_flag_number_map(self) -> None:
        # Create map between flag numbers and flag names;
        for i, flag_name in enumerate(
                self._ingredient_service.current_ingredient.flag_data.keys(), start=1):
            self._flag_number_map[i] = flag_name

    def _deterimine_state(self) -> None:
        if not self._asked_cycle:
            self._state = 'ask_cycle'
        elif self._cycling == True:
            if self._current_flag_number >= len(self._flag_number_map):
                self._state = 'cycle_finished'
            else:
                self._state = 'cycle_set_flag'
        elif not self._current_flag_number:
            self._state = 'select_flag'
        else:
            self._state = 'menu_set_flag'


    def run(self) -> str:
        # Update the ingredient data in the window;
        self.app.set_window_text(self._ingredient_service.summarise_ingredient(
            self._ingredient_service.current_ingredient
        ))
        self.app.show_text_window()
        # Select state;
        self._determine_state()
        # Prepare a string to hold the output;
        output = ''
        # Go for it!;
        if self._state == 'ask_cycle':
            output = _SET_ALL_FLAGS_QUESTION
        elif self._state == 'cycle_set_flag' or \
                self._state == 'menu_set_flag':
            output = _FLAG_EDITOR.format(
                ingredient_name=self._ingredient_service.current_ingredient.name,
                flag=self.flag_number_map[self._current_flag_number]
            )
        elif self._state == 'select_flag':
            for option_number in self._flag_number_map.keys():
                output = output + _FLAG_MENU_ITEM.\
                    format(
                        flag_number=option_number,
                        flag=self._flag_number_map[option_number]
                    )
            output = _FLAG_MENU.format(output)
        elif self._state == 'cycle_finished':
            output = _FLAGS_SET_CONFIRMATION
        # Wrap the output in the standard page & return;
        output = self.run_parent('StandardPage', output)
        return output

    def dynamic_response(self, response) -> None:
        if self._state == 'ask_cycle':
            if response == 'y':
                self._cycling = True
            elif response == 'n':
                self._cycling = False
            self.asked_cycle = True
        elif self._state == 'cycle_set_flag':
            if response == 'y':
                self._ingredient_service.current_ingredient.set_flag(
                    self._flag_number_map[self._current_flag_number],
                    True
                )
            elif response == 'n':
                self._ingredient_service.current_ingredient.set_flag(
                    self._flag_number_map[self._current_flag_number],
                    True
                )
            if response == 'y' or response == 'n':
                self._current_flag_number = self._current_flag_number + 1
        elif self._state == 'menu_set_flag':
            if response == 'y':
                self._ingredient_service.current_ingredient.set_flag(
                    self._flag_number_map[self._current_flag_number],
                    True
                )
            elif response == 'n':
                self._ingredient_service.current_ingredient.set_flag(
                    self._flag_number_map[self._current_flag_number],
                    True
                )
        elif self._state == 'select_flag':
            if response in self._flag_number_map.keys():
                self._current_flag_number = response
        elif self._state == 'cycle_finished':
            if response == 'o':
                self.app.navigate_back()           
