from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service
    from pydiet.cli.ingredients import ingredient_edit_service

_MENU_TEMPLATE = '''Choose an option:
(1) -- Manage ingredients.
(2) -- Manage recipes.
(3) -- Manage user goals.
(4) -- Run optimiser.
'''


class MainMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self.set_option_response('1', self.on_manage_ingredients)
        self.set_option_response('2', self.on_manage_recipes)
        self.set_option_response('3', self.on_manage_goals)
        self.set_option_response('4', self.on_run_optimiser)

    def print(self):
        output = _MENU_TEMPLATE
        output = self.get_component('standard_page_component').print(output)
        return output

    def on_manage_ingredients(self):
        # Navigate;
        self.goto('.ingredients')

    def on_manage_recipes(self):
        raise NotImplementedError

    def on_manage_goals(self):
        raise NotImplementedError

    def on_run_optimiser(self):
        raise NotImplementedError
