from pyconsoleapp import ConsoleAppComponent

from pydiet.optimisation import global_day_goals

_MAIN = '''Global Day Goals:
------------------

Max Daily Food Cost: £{cost}              | -cost [cost]
Daily Calorie Goal: {cals}cals            | -cals [calories]
Percentage Daily Fat: {perc_fat}%         | -pfat [percentage]
Percentage Daily Protein: {perc_prot}%    | -pprt [percentage]
Percentage Daily Carbs: {perc_carbs}%     | -pcrb [percentage]

-f -> Edit global flags.
-n -> Edit global nutrient targets.
-s -> Save changes.

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
        self.set_response_function(['-f'], self.on_edit_flags)
        self.set_response_function(['-n'], self.on_edit_nutrient_targets)
        self.set_response_function(['-s'], self.on_save)

    def print(self, *args, **kwargs) -> str:
        return _MAIN.format(
            cost=self._gdg.max_cost_gbp,
            cals=self._gdg.calories,
            perc_fat=self._gdg.perc_fat,
            perc_carbs=self._gdg.perc_carbs,
            perc_prot=self._gdg.perc_protein
        )

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
        self.app.goto('home.goals.edit_globals.edit_flags')

    def on_edit_nutrient_targets(self):
        self.app.goto('home.goals.edit_globals.edit_nutrient_targets')

    def on_save(self):
        try:
            self._gdg.save()
        except PercentageSumError:
            self.app.error_message = 'The primary macro percentages must sum to 100%'