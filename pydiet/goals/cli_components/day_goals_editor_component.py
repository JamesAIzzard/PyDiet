from typing import Dict, TYPE_CHECKING, cast

from pyconsoleapp import ConsoleAppComponent, menu_tools, parse_tools

from pydiet.optimisation import optimisation_edit_service as oes
from pydiet.optimisation import meal_goals
from pydiet.optimisation.exceptions import DuplicateDayGoalsNameError, DuplicateMealGoalsNameError

if TYPE_CHECKING:
    from pydiet.optimisation.day_goals import DayGoals
    from pydiet.optimisation.cli_components.meal_goals_editor_component import MealGoalsEditorComponent

_MAIN = '''
-n, -name [Day Name]    | {plan_name}:

Meal Name               Ratios     Cals
------------------------------------------------------
1. Breakfast            | 30-30-40 | 800cals
2. Lunch                | 30-30-40 | 1200cals
3. Dinner               | 30-30-40 | 1600cals
{meals}
------------------------------------------------------
Where ratio is : protein-carb-fat

-add, -a    [meal name]   -> Add a meal.
-edit, -e   [meal number] -> Edit a meal.
-delete, -d [meal number] -> Delete a meal.
-manage, -m               -> Manage the day's nutrient targets.
-save, -s                 -> Save changes.

'''
_MEAL_TEMPLATE = '{num}. {meal_name} | {ratios} | {cals}cals\n'
_RATIO_TEMPLATE = '{perc_prot}-{perc_fat}-{perc_carbs}'


class DayGoalsEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.subject:'DayGoals'
        self.meal_goals_number_name_map: Dict[int, str] = {}
        self.set_print_function(self.print)
        self.set_response_function(['-name', '-n'], self.on_set_name)
        self.set_response_function(['-add', '-a'], self.on_add_meal)
        self.set_response_function(['-save', 's'], self.on_save)

    def before_print(self) -> None:
        # Create a numbered list of the MealGoals names on the DayGoals;
        self.meal_goals_number_name_map = menu_tools.create_number_name_map(
            list(self.subject.meal_goals.keys()))

    @property
    def meal_summary_table(self) -> str:
        # If there are no meal goals yet;
        if not len(self.subject.meal_goals):
            return 'No meals added yet.'
        # Otherwise, build the meal summary;
        else:
            output = ''
            # Iterate through the number map;
            for num in self.meal_goals_number_name_map.keys():
                # Grab the meal goals instance;
                mg = self.subject.meal_goals[self.meal_goals_number_name_map[num]]
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

    def print(self) -> str:
        # Create the content;
        output = _MAIN.format(
            plan_name=self.subject.name,
            meals=self.meal_summary_table
        )
        # Format and return the template;
        output = self.app.fetch_component(
            'standard_page_component').call_print(
                page_title='Day Goals Editor',
                page_content=output)
        return output

    def on_set_name(self, name:str) -> None:
        try:
            self.subject.name = name
        except DuplicateDayGoalsNameError:
            self.app.error_message = 'There is already a day called {day_goals_name}'.format(
                day_goals_name=name)
            return

    def on_add_meal(self, meal_name:str=None)->None:
        # Check the meal name was provided;
        if not meal_name:
            self.app.error_message = 'The meal name must be provided.'
            return

        # Try to add a fresh mealgoals instance to the daygoals;
        try:
            mg = self.subject.add_new_meal_goal(meal_name)
        except DuplicateMealGoalsNameError:
            self.app.error_message = '{day_name} already contains a meal called {meal_name}'.format(
                day_name=self.subject.name,
                meal_name=meal_name
            )
            return

        # Configure the mealgoals editor;
        mge = cast('MealGoalsEditorComponent', self.app.fetch_component('meal_goals_editor_component'))
        mge.subject = mg

        # Navigate to the mealgoals editor:
        self.app.goto('home.goals.edit_day.edit_meal')


    def on_save(self) -> None:
        self._oes.save_changes()

