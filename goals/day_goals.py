from typing import Optional, List, Dict

from model import nutrients, quantity
import persistence
import goals


class DayGoalsData(goals.GoalsData):
    name: Optional[str]
    solution_datafile_names: List[str]
    meal_goals: Dict[str, 'goals.MealGoalsData']


class DayGoals(goals.HasSettableGoals, persistence.SupportsPersistence):
    """Models a set of nutrient goals associated with a day."""

    def __init__(self, day_goals_data: Optional['DayGoalsData'] = None, **kwargs):
        super().__init__(**kwargs)
        self._meal_goals: Dict[str, 'goals.MealGoals'] = {}

    @property
    def name(self) -> str:
        """Returns the unique name of the DayGoals instance."""
        return self.unique_value

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self.unique_value = name

    def set_nutrient_mass_goal(self, nutrient_name: str, nutrient_mass: Optional[float] = None,
                               nutrient_mass_unit: str = 'g') -> None:
        """Extends the ABC's nutrient mass goal setter to also check that the
        sum of any child MealGoal targets for the same nutrient is not lower."""
        # Validate inputs;
        nutrient_name = nutrients.validation.validate_nutrient_name(nutrient_name)

        # If we are unsetting;
        if nutrient_mass is None:
            super().set_nutrient_mass_goal(nutrient_name, None)
            return

        # We are not unsetting, so validate the quantity parameters;
        nutrient_mass = quantity.validation.validate_quantity(nutrient_mass)
        nutrient_mass_unit = quantity.validation.validate_mass_unit(nutrient_mass_unit)

        # Check we can set without overconstraining MealGoals;
        if len(self.meal_goals):  # Only required if we actually have child MealGoals.
            unconstrained: int = 0
            for meal_goals in self.meal_goals.values():
                if meal_goals.get_nutrient_mass_goal(nutrient_name) is None:
                    unconstrained = unconstrained + 1
            if unconstrained == 0:
                raise goals.exceptions.OverConstrainedNutrientMassGoalError()

        # Convert mass target to grams;
        nutrient_mass_g = quantity.convert_qty_unit(
            qty=nutrient_mass,
            start_unit=nutrient_mass_unit,
            end_unit='g'
        )

        # Sum up any meal goal nutrient masses;
        total_mg_mass = 0
        for meal_goal in self._meal_goals.values():
            mg_mass = meal_goal.get_nutrient_mass_goal(nutrient_name, 'g')
            if mg_mass is not None:
                total_mg_mass = total_mg_mass + mg_mass

        # Exception if MealGoals total mass exceeds DayGoal target mass;
        if total_mg_mass > nutrient_mass_g:
            raise goals.exceptions.ConflictingNutrientMassGoalError()

        # No issues, so go ahead and set;
        super().set_nutrient_mass_goal(nutrient_name, nutrient_mass, nutrient_mass_unit)

    @property
    def meal_goals(self) -> Dict[str, 'goals.MealGoals']:
        """Returns a dict of the MealGoals instances associated with this DayGoals instance."""
        return self._meal_goals

    def add_meal_goals(self, meal_goals: List['goals.MealGoals']) -> None:
        """Adds MealGoals instances to the DayGoals.
        Note:
            Requires that each MealGoals instance has a unique name.
        """
        for meal_goal in meal_goals:
            # Catch absent name;
            if meal_goal.name is None:
                raise goals.exceptions.UnnamedMealGoalError()
            # Catch duplicated name;
            if meal_goal.name in self._meal_goals.keys():
                raise goals.exceptions.MealGoalNameClashError()

        # All OK, go ahead and add references and add to list;
        for meal_goal in meal_goals:
            # Place reference to DayGoal in MealGoal
            meal_goal.parent_day_goal = self
            # Add the MealGoal instance;
            self._meal_goals[meal_goal.name] = meal_goal

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.day_goals_db_path

    @property
    def persistable_data(self) -> 'DayGoalsData':
        return DayGoalsData(
            name=self.name,
            solution_datafile_names=[],
            flags={},
            max_cost_gbp_target=30.00,
            calorie_target=3000,
            nutrient_mass_targets={},
            meal_goals={}
        )

    def load_data(self, day_goals_data: 'DayGoalsData') -> None:
        self.unique_value = day_goals_data["name"]
