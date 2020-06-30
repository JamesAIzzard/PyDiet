from typing import Dict, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, menu_tools, parse_tools

from pydiet.optimisation import optimisation_edit_service as oes
from pydiet.optimisation import meal_goals
from pydiet.optimisation.exceptions import DuplicateDayGoalsNameError, DuplicateMealGoalsNameError

if TYPE_CHECKING:
    from pydiet.optimisation.day_goals import DayGoals

_MAIN = '''
(-n [Day Name])         | {plan_name}:

Meal Name               Ratios     Cals
------------------------------------------------------
1. Breakfast            | 30-30-40 | 800cals
2. Lunch                | 30-30-40 | 1200cals
3. Dinner               | 30-30-40 | 1600cals
{meals}
------------------------------------------------------
Where ratio is : protein-carb-fat

(-a [meal name])   -> Add a meal.
(-e [meal number]) -> Edit a meal.
(-d [meal number]) -> Delete a meal.
(-m)               -> Manage the day's nutrient targets.
(-s)               -> Save changes.

'''
_MEAL_TEMPLATE = '{num}. {meal_name} | {ratios} | {cals}cals\n'
_RATIO_TEMPLATE = '{perc_prot}-{perc_fat}-{perc_carbs}'


class DayGoalsEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._oes = oes.OptimisationEditService()
        self.meal_goals_number_name_map: Dict[int, str] = {}
        self.set_option_response('-s', self.on_save)

    def run(self) -> None:
        # Create a numbered list of the MealGoals names on the DayGoals;
        self.meal_goals_number_name_map = menu_tools.create_number_name_map(
            list(self._oes.day_goals.meal_goals.keys()))

    def print_meals(self, day_goals: 'DayGoals') -> str:
        # If there are no meal goals yet;
        if not len(day_goals.meal_goals):
            return 'No meals added yet.'
        # Otherwise, build the meal summary;
        else:
            output = ''
            # Iterate through the number map;
            for num in self.meal_goals_number_name_map.keys():
                # Grab the meal goals instance;
                mg = self._oes.day_goals.meal_goals[self.meal_goals_number_name_map[num]]
                # Build the line;
                output = output + _MEAL_TEMPLATE.format(
                    num=num,
                    meal_name=mg.name,
                    ratios=_RATIO_TEMPLATE.format(
                        perc_prot=mg.perc_protein,
                        perc_fat=mg.perc_fat,
                        perc_carbs=mg.perc_carbs
                    ),
                    cals=mg.calories
                )
            # Return;
            return output

    def print(self, *args, **kwargs) -> str:
        # Check the right stuff is on the oes;
        if not self._oes.day_goals:
            raise AttributeError
        # Create the content;
        output = _MAIN.format(
            plan_name=self._oes.day_goals.name,
            meals=self.print_meals(self._oes.day_goals)
        )
        # Format and return the template;
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def dynamic_response(self, raw_response: str) -> None:
        # Check there is a day_goals in scope;
        if not self._oes.day_goals:
            raise AttributeError
        # Parse the input as a flags and text;
        flags, text = parse_tools.parse_flags_and_text(raw_response)

        # If we are renaming the day;
        if flags == ['-n']:
            # Check the day name is provided;
            if not text:
                self.app.error_message = 'Please specify a new day name.'
                return
            # Try set the name;
            try:
                self._oes.day_goals.name = text
            except DuplicateDayGoalsNameError:
                self.app.error_message = 'The name {dg_name} is already assigned to another day.'.format(dg_name=text)

        # If we are adding a new meal;
        elif flags == ['-a']:
            # Check the name is provided;
            if not text:
                self.app.error_message = 'The meal name must be provided.'
                return
            # Get a fresh MealGoals instance;
            mg = meal_goals.MealGoals(text, self._oes.day_goals)
            try:
                # Put a fresh MealGoals instance on scope;
                self._oes.day_goals.add_meal_goal(text, mg)
            except DuplicateMealGoalsNameError:
                self.app.error_message = '{day_name} already includes a meal called {meal_name}'.format(
                    day_name=self._oes.day_goals.name,
                    meal_name=text
                )
            # Navigate to the meal_editor;
            self.app.goto('home.goals.edit_day.edit_meal')

    def on_save(self) -> None:
        self._oes.save_changes()

