from pydiet.ingredients.exceptions import FlagNutrientConflictError
from typing import cast, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent

from pydiet.optimisation import global_day_goals
from pydiet.optimisation.exceptions import PercentageSumError

if TYPE_CHECKING:
    from pydiet.cli_components.flag_editor_component import FlagEditorComponent

_MAIN = '''Global Day Goals:
------------------

Max Daily Food Cost:   {cost:>10} | -cost [cost]
Daily Calorie Goal:    {cals:>10} | -cals [calories]
Perc Daily Fat:        {perc_fat:>10} | -pfat [percentage]
Perc Daily Protein:    {perc_protein:>10} | -pprt [percentage]
Perc Daily Carbs:      {perc_carbs:>10} | -pcrb [percentage]

-flags, -f  -> Edit global flags.
-nuts, -n   -> Edit global nutrient targets.
-save, -s   -> Save changes.

'''


class GlobalDayGoalsEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._gdg = global_day_goals.GlobalDayGoals()
        self.set_response_function(['-cost'], self.on_edit_cost)
        self.set_response_function(['-cals'], self.on_edit_cals)
        self.set_response_function(['-pfat'], self.on_edit_perc_fat)
        self.set_response_function(['-pprt'], self.on_edit_perc_protein)
        self.set_response_function(['-pcrb'], self.on_edit_perc_carbs)
        self.set_response_function(['-flags', '-f'], self.on_edit_flags)
        self.set_response_function(['nuts', '-n'], self.on_edit_nutrient_targets)
        self.set_response_function(['-save', '-s'], self.on_save)

    def print(self, *args, **kwargs) -> str:
        output = _MAIN.format(
            cost='£'+str(format(self._gdg.max_cost_gbp, '.2f')) if self._gdg.max_cost_gbp else 'Undefined',
            cals=str(self._gdg.calories)+'cals' if self._gdg.calories else 'Undefined',
            perc_fat=str(self._gdg.perc_fat)+'%' if self._gdg.perc_fat else 'Undefined',
            perc_protein=str(self._gdg.perc_protein)+'%' if self._gdg.perc_protein else 'Undefined',
            perc_carbs=str(self._gdg.perc_carbs)+'%' if self._gdg.perc_carbs else 'Undefined'
        )
        return self.app.fetch_component('standard_page_component').print(output)

    def on_edit_cost(self, args):
        try:
            self._gdg.max_cost_gbp = args
        except ValueError:
            self.app.error_message = 'The cost must be a positive decimal value.'

    def on_edit_cals(self, args):
        try:
            self._gdg.calories = args
        except ValueError:
            self.app.error_message = 'Calories must be a positive decimal value.'

    def on_edit_perc_fat(self, args):
        try:
            self._gdg.perc_fat = args
        except ValueError:
            self.app.error_message = 'Percentage fat must be a positive decimal value between 0-100.'

    def on_edit_perc_carbs(self, args):
        try:
            self._gdg.perc_carbs = args
        except ValueError:
            self.app.error_message = 'Percentage carbs must be a positive decimal value between 0-100.'

    def on_edit_perc_protein(self, args):
        try:
            self._gdg.perc_protein = args
        except ValueError:
            self.app.error_message = 'Percentage protein must be a positive decimal value between 0-100.'

    def on_edit_flags(self):
        # Place the day goals object on the flag editor;
        cast('FlagEditorComponent', self.app.fetch_component('flag_editor_component')).subject = self._gdg
        # Redirect to the flag editor;
        self.app.goto('home.goals.edit_globals.edit_flags')

    def on_edit_nutrient_targets(self):
        self.app.goto('home.goals.edit_globals.edit_nutrient_targets')

    def on_save(self):
        # Attempt the save and handle exceptions;
        try:
            self._gdg.save()
        except PercentageSumError:
            self.app.error_message = 'The primary macro percentages must sum to 100%'
        # Inform the user;
        self.app.info_message = 'Global day goals saved.'
        
