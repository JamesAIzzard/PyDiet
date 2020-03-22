from typing import TYPE_CHECKING
from pinjector import inject
from pyconsoleapp.console_app_component import ConsoleAppComponent
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.ingredients.ingredient_service import IngredientService

_TEMPLATE = '''Choose an option:
(s) - Save the ingredient.
(1) - Set ingredient name.
(2) - Set ingredient cost.
(3) - Set ingredient flags.
(4) - Set macronutrient totals.
(5) - Set a macronutrient.
(6) - Set a micronutrient.
'''


class IngredientEditMenu(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ingredient_service:'IngredientService' = inject('ingredient_service')
        self.set_option_response('1', self.on_set_name)
        self.set_option_response('2', self.on_set_cost)
        self.set_option_response('3', self.on_set_flags)
        self.set_option_response('4', self.on_set_macro_totals)

    def print(self):
        # Draw the view;
        output = _TEMPLATE
        output = self.app.get_component('StandardPage').print(output)
        return output

    def on_set_name(self):
        self.app.show_text_window()
        self.app.navigate(['.', 'name'])

    def on_set_cost(self):
        self.app.show_text_window()
        scope = self.get_scope('ingredient_edit')
        # Fresh some scope vars to determine
        # state of cost setting and store data;
        scope.cost_mass = None
        scope.cost_mass_units = None
        scope.cost = None
        # Go set the cost;
        self.app.navigate(['.', 'cost_mass'])

    def on_set_flags(self):
        # Show the window;
        self.app.show_text_window()
        scope = self.get_scope('ingredient_edit')
        # Create flag data properties;
        scope.current_flag_number = 0
        scope.cycling_flags = False
        # Build the flag map;
        flag_number_map = {}
        for i, flag_name in enumerate(
                scope.ingredient.flag_data.keys(), start=1):
            flag_number_map[str(i)] = flag_name
        scope.flag_number_map = flag_number_map        
        # Helper functions to get current flag name;
        def current_flag_name(scope):
            return scope.get_flag_name(scope.current_flag_number, scope)
        def get_flag_name(flag_number, scope):
            return scope.flag_number_map[str(flag_number)]
        scope.current_flag_name = current_flag_name    
        scope.get_flag_name = get_flag_name    
        # If the ingredient has no name, prompt the user for it first;
        if not scope.ingredient.name:
            self.app.error_message = 'Ingredient name must be set first.'
        # The name is set;
        else:
            # If all flags undefined, ask to cycle;
            if scope.ingredient.all_flags_undefined:
                self.app.navigate(['.', 'flags', 'set_all?'])
            # Otherwise, just show the flag menu;
            else:
                self.app.navigate(['.', 'flags'])

    def on_set_macro_totals(self):
        scope = self.get_scope('ingredient_edit')
        # Show the window;
        self.app.show_text_window()
        # Create the nutrient proeprties;
        scope.nutrient_number_map = {}
        # Helper functions
        def get_nutrient_name(number, scope):
            return scope.nutrient_number_map[str(number)]
        scope.get_nutrient_name = get_nutrient_name
        # Build the nutrient number map;
        ingredient:'Ingredient' = scope.ingredient
        for i, nutrient_name in enumerate(ingredient.\
            macronutrient_totals_data.keys(), start=1):
            scope.nutrient_number_map[str(i)] = nutrient_name
        # If the ingredient has no name, prompt the user for it first;
        if not scope.ingredient.name:
            self.app.error_message = 'Ingredient name must be set first.'
        # The name is set;
        else:
            # Navigate to the macro totals menu;
            self.app.navigate(['.', 'macro_totals'])
