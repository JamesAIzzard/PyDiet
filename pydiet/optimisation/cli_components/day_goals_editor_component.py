from typing import Dict, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, menu_tools

from pydiet.optimisation import optimisation_edit_service as oes

if TYPE_CHECKING:
    from pydiet.optimisation.day_goals import DayGoals

_MAIN = '''{plan_name}:

   Name                   Ratios     Cals
------------------------------------------------------
1. Breakfast            | 30-30-40 | 800cals
2. Lunch                | 30-30-40 | 1200cals
3. Dinner               | 30-30-40 | 1600cals
{meals}
------------------------------------------------------
Where ratio is : protein-carb-fat

(a)   -- Add a meal.
(e-*) -- Edit a meal.
(d-*) -- Delete a meal.
(m)   -- Manage day micronutrient targets.

'''
_MEAL_TEMPLATE = '{num}. {meal_name} | {ratios} | {cals}cals\n'
_RATIO_TEMPLATE = '{perc_prot}-{perc_fat}-{perc_carbs}'


class DayGoalsEditorComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._oes = oes.OptimisationEditService()
        self.meal_goals_number_name_map: Dict[int, str] = {}

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

    def print_ratios(self, meal_goals: 'MealGoals') -> str:
        raise NotImplementedError

    def print(self, *args, **kwargs) -> str:
        # Create the content;
        output = _MAIN.format(
            plan_name=self._oes.day_goals.name,
            meals=self.print_meals(self._oes.day_goals)
        )
        # Format and return the template;
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output
